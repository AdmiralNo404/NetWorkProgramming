import java.net.*;
import java.io.*;
import java.util.*;

public class ProxyServer extends Thread {
	static final int BUFSZ = 8192;
	
	Socket s;
	String host;
	int port;
	OutputStream rawOut;
	InputStream rawIn;
	Socket serverConnection;
	byte requestBuffer[] = new byte[BUFSZ];
	int storedCount = 0;
	int consumedCount = 0;
	String cfgFile;
	
	ProxyServer (String cfgFile, Socket s) {
		System.out.println("New client.");
		this.cfgFile = cfgFile;
		this.s = s;
	}
	
	protected Socket connectToServer() throws IOException {
		System.out.println("Connecting to " + host + ":" + port + "..");
		Socket socket = new Socket(host, port);
		System.out.println("Connected.");

		rawOut = socket.getOutputStream();
		rawIn = socket.getInputStream();
		return socket;
	}
	
	public void run() {
		StringTokenizer st;
		URL resourceURL;

		/******************************************************************/
		ByteArrayOutputStream headerBuf = new ByteArrayOutputStream(BUFSZ);
		PrintWriter headerWriter = new PrintWriter(headerBuf);
		/*******************************************************************/
		ByteArrayOutputStream respBuf = new ByteArrayOutputStream(BUFSZ);
		PrintWriter respWriter = new PrintWriter(respBuf);
		/*******************************************************************/
		
		try {
			// open and read the config file
			FileReader fr = new FileReader(cfgFile);
			BufferedReader fbr = new BufferedReader(fr);
			// make a block list
			HostList blocked = new HostList();
			String fline = "";
			while ((fline = fbr.readLine()) != null) {
				fline = fline.trim();
				if (fline.startsWith("#") || fline.equals("")) {
					continue;
				}
				// parse the string for host and types
				StringTokenizer tempst = new StringTokenizer(fline);
				String bhost = tempst.nextToken();
				String btype;
				if (tempst.hasMoreTokens()) {
					btype = tempst.nextToken();
				} else {
					btype = "*";
				}
				
				blocked.add(bhost, btype);
			}
			fbr.close();
			fr.close();
			
			InputStream istream = s.getInputStream();
			OutputStream ostream = s.getOutputStream();

			BufferedReader br = new BufferedReader(new InputStreamReader(istream));
			
			//System.out.println("Reading HTML Request...");
			String requestLine;
			String resourcePath;
			String filePath = "";
			String urlPath;

			String line = "";
			if ((line = br.readLine()) != null) {
				requestLine = line;
			} else {
				throw new IOException("End of buffer!");
			}
			System.out.println(requestLine);
			headerWriter.println(requestLine);
			
			st = new StringTokenizer(requestLine);
			String request = st.nextToken(); /* GET, POST, HEAD */
			
			//System.out.println("#DEBUG MESSAGE: Request Method =" + request);
			
			if (request.equals("GET") || request.equals("HEAD")) {
				// System.out.println("Request = " + request);

				String uri = st.nextToken(); /* / URI */
				String protocol = st.nextToken(); /* HTTP1.1 or HTTP1.0 */

				if (uri.startsWith("http")) {
					/* It is a full URL. So get the file path */
					resourceURL = new URL(uri);
					filePath = resourceURL.getPath();
					host = resourceURL.getHost();
					port = resourceURL.getPort();
					if (port == -1) {
						port = 80;
					}
					System.out.println("#DEBUG MESSAGE:  Request URI = " + filePath);
				}
				urlPath = uri;
				
				if ((line = br.readLine()) != null) {
					requestLine = line;
				} else {
					throw new IOException("End of buffer!");
				}
				
				st = new StringTokenizer(requestLine, ": ");
				String fieldName = st.nextToken(); /* Expect HOST field */

				if (fieldName.equals("Host")) {
					host = st.nextToken();
					String portString = new String("");
					;
					try {
						portString = st.nextToken();
					} catch (Exception NoSuchElement) {
					}
					if (portString.length() == 0) {
						port = 80;
					} else
						port = Integer.parseInt(portString);

					System.out.println("#DEBUG MESSAGE  - Host = " + host + " port number = " + port);
				}

				while (requestLine.length() != 0) {
					headerWriter.println(requestLine);
					//System.out.println(requestLine);
					if ((line = br.readLine()) != null) {
						requestLine = line;
					} else {
						throw new IOException("End of buffer!");
					}
				}

				headerWriter.flush();
				
				//System.out.println("Reading complete.");
				// end getting request
				
				/***********************************************************************
				// print the header for debug uses
				System.out.println("******** Buffered Headers for debugging  **************");
				System.out.print(headerBuf.toString());
				System.out.println("******** End of Buffered Headers for debugging  **************");
				/*************************************************************************/
				
				// open a log file to log the headers
				try(PrintWriter pwout = new PrintWriter(new BufferedWriter(new FileWriter("log.txt", true)))) {
					pwout.println(headerBuf.toString());
				}catch (IOException e) {
					e.printStackTrace();
				}
				
				/********************************************************************************/
				/* Open connection to the server host */
				/********************************************************************************/

				String terminator = new String("Connection:close\n\n");
				serverConnection = connectToServer();
				
				rawOut.write((headerBuf.toString()).getBytes());
				rawOut.write(terminator.getBytes());
				
				byte buffer[] = new byte[BUFSZ];
				int count;
				// a string to store server response header
				String respHeader = "";
				// another string to store content type
				String contType = "";
				// indicator of header reading process
				boolean hasReadHeader = false;
				while ((count = rawIn.read(buffer, 0, BUFSZ)) > -1) {
					// read the header of the server response
					String serverResp = new String(buffer, "UTF-8");
					BufferedReader sbr = new BufferedReader(new StringReader(serverResp));
					String respLine = "";
					if (!hasReadHeader) {
						while ((respLine = sbr.readLine()) != null) {
							if (respLine.length() == 0) {
								hasReadHeader = true;
								break;
							}
							respHeader = respHeader + respLine + "\n";
							if (respLine.startsWith("Content-Type")) {
								StringTokenizer tempst = new StringTokenizer(respLine);
								tempst.nextToken();
								contType = tempst.nextToken();
							}
						}
					}
					//System.out.println(respHeader);
					// log the response header to log file
					try(PrintWriter pwout = new PrintWriter(new BufferedWriter(new FileWriter("log.txt", true)))) {
						pwout.println(respHeader);
					}catch (IOException e) {
						e.printStackTrace();
					}
					
					System.out.println(contType);
					
					if (hasReadHeader) {
					// check if the host is in blocked list
						if (blocked.contains(host)) {
							// check the content type
							TypeList btypes = blocked.getType(host);
							System.out.println(btypes.contains(contType));
							if (btypes.head.type.equals("*")) {
								// which means all contents blocked
								respWriter.println("HTTP/1.1 403 Forbidden");
								respWriter.println("Connection: Close\n");
								respWriter.println("<!DOCTYPE html>");
								respWriter.println("<html>");
								respWriter.println("<head><title>403 Forbidden</title></head>");
								respWriter.println("<body><h1>403 Forbidden</h1></body>");
								respWriter.println("</html>");
								respWriter.flush();
								ostream.write((respBuf.toString()).getBytes());
								
								try(PrintWriter pwout = new PrintWriter(new BufferedWriter(new FileWriter("log.txt", true)))) {
									pwout.println(host + "::blocked");
								}catch (IOException e) {
									e.printStackTrace();
								}
								
								System.out.println("Client exit.");
								System.out.println("---------------------------------------------------");
								serverConnection.close();
								s.close();
								return;
							} else if (btypes.contains(contType)) {
								// which means the content type is blocked
								respWriter.println("HTTP/1.1 403 Forbidden");
								respWriter.println("Connection: Close\n");
								respWriter.println("<!DOCTYPE html>");
								respWriter.println("<html>");
								respWriter.println("<head><title>403 Forbidden</title></head>");
								respWriter.println("<body><h1>403 Forbidden</h1></body>");
								respWriter.println("</html>");
								respWriter.flush();
								ostream.write((respBuf.toString()).getBytes());
								
								try(PrintWriter pwout = new PrintWriter(new BufferedWriter(new FileWriter("log.txt", true)))) {
									pwout.println(host + filePath + "::File type not allowed");
								}catch (IOException e) {
									e.printStackTrace();
								}
								
								System.out.println("Client exit.");
								//System.out.println("Blocked " + contType);
								System.out.println("---------------------------------------------------");
								serverConnection.close();
								s.close();
								return;
							}
						}
					}
					
					// else forward the response to client
					ostream.write(buffer, 0, count);
				}
			} else {
				respWriter.println("HTTP/1.1 406 Not Acceptable");
				respWriter.println("Connection: Close\n");
				respWriter.println("<!DOCTYPE html>");
				respWriter.println("<html>");
				respWriter.println("<head><title>406 Not Acceptable</title></head>");
				respWriter.println("<body><h1>406 Not Acceptable</h1></body>");
				respWriter.println("</html>");
				respWriter.flush();
				/***********************************************************************
				// print the header for debug uses
				System.out.println("******** Buffered Headers for debugging  **************");
				System.out.print(headerBuf.toString());
				System.out.println("******** End of Buffered Headers for debugging  **************");
				/*************************************************************************/
				ostream.write((respBuf.toString()).getBytes());
			}

			System.out.println("Client exit.");
			System.out.println("---------------------------------------------------");
			if (serverConnection != null) { serverConnection.close(); }
			s.close();
			
		} catch (IOException ex) {
			ex.printStackTrace();
		}
	}
	
	public static void main (String args[]) {
		try {
			String config = args[0];
			int port = Integer.parseInt(args[1]);
			System.out.println(config + " " + port);
			
			// create welcome socket
			System.out.println("Starting on port " + port);
			ServerSocket sSock = new ServerSocket(port);
			
			while (true) {
				System.out.println("Waiting for a client request");
				Socket cSock = sSock.accept();
				System.out.println("Received request from " + cSock.getInetAddress());
				ProxyServer p = new ProxyServer(config, cSock);
				p.start();
			}
		} catch (IndexOutOfBoundsException|NumberFormatException ex) {
			// input validation
			System.out.println("Syntax: " + ProxyServer.class.getSimpleName() + " <config-file-name> <port-number>");
		} catch (RuntimeException ex) {
			ex.printStackTrace();
		} catch (IOException ex) {
			ex.printStackTrace();
		}
	}
	
}
