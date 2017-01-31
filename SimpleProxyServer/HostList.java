public class HostList {
	HostNode head;
	
	HostList(String host, String type) {
		this.head = new HostNode(host, type);
	}
	
	HostList() {
		this.head = null;
	}
	
	public void add(String host, String type) {
		HostNode cur = head;
		if (cur == null) {
			head = new HostNode(host, type);
			return;
		}
		while (cur.next != null) {
			if (cur.host.equals(host)) {
				cur.addType(type);
				return;
			}
			cur = cur.next;
		}
		cur.next = new HostNode(host, type);
	}
	
	public TypeList getType(String host) {
		HostNode cur = head;
		while (cur != null) {
			if (cur.host.equals(host)) {
				return cur.types;
			}
			cur = cur.next;
		}
		return null;
	}
	
	public boolean contains(String host) {
		HostNode cur = head;
		if (cur == null) {
			return false;
		}
		while (cur != null) {
			if (cur.host.equals(host)) {
				return true;
			}
			cur = cur.next;
		}
		return false;
	}
}

class HostNode {
	String host;
	TypeList types;
	HostNode next;
	
	HostNode (String host, String type) {
		this.host = host;
		types = new TypeList(type);
		next = null;
	}
	
	public void addType(String type) {
		types.add(type);
	}
}

class TypeList {
	TypeNode head;
	
	TypeList (String type) {
		head = new TypeNode(type);
	}
	
	public void add(String type) {
		if (type.equals("*") || type.equals("*/*")) {
			head = new TypeNode("*");
			return;
		}
		TypeNode cur = head;
		if (cur.type.equals("*") || cur.type.equals("*/*")) {
			return;
		}
		while (cur.next != null) {
			if (cur.type.equals(type)) {
				return;
			}
			cur = cur.next;
		}
		cur.next = new TypeNode(type);
	}
	
	public boolean contains(String type) {
		TypeNode cur = head;
		if (cur == null) {
			return false;
		}
		while (cur != null) {
			if (cur.type.equals(type)) {
				return true;
			}
			// parse the type strings for special case e.g. image/* vs image/gif
			String[] r1 = type.split("/");
			String[] r2 = cur.type.split("/");
			if (r2.length == 1) {
				return true;
			}
			if (r1[0].equals(r2[0]) && r2[1].equals("*")) {
				return true;
			}
			cur = cur.next;
		}
		return false;
	}
}

class TypeNode {
	String type;
	TypeNode next;
	
	TypeNode (String type) {
		this.type = type;
		next = null;
	}
}
