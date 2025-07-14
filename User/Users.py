from typing import List, Tuple, Optional

class Node:
    def __init__(self, username: str, score: int):
        self.username = username
        self.score = score
        self.next: Optional['Node'] = None

class LeaderboardLinkedList:
    def __init__(self):
        self.head: Optional[Node] = None

    def insert_sorted(self, username: str, score: int) -> None:
        """Insert a new node in descending score order"""
        new_node = Node(username, score)

        # Insert at head if empty or new score is highest
        if not self.head or score > self.head.score:
            new_node.next = self.head
            self.head = new_node
            return

        # Find insertion point
        current = self.head
        while current.next and current.next.score >= score:
            current = current.next

        # Insert new node
        new_node.next = current.next
        current.next = new_node

    def remove_user(self, username: str) -> bool:
        """Remove a user from the linked list"""
        if not self.head:
            return False

        # Special case: head node
        if self.head.username == username:
            self.head = self.head.next
            return True

        # Search for node to remove
        current = self.head
        while current.next:
            if current.next.username == username:
                current.next = current.next.next
                return True
            current = current.next

        return False  # User not found

    def to_list(self) -> List[Tuple[str, int]]:
        """Convert linked list to list of (username, score) tuples"""
        result = []
        current = self.head
        while current:
            result.append((current.username, current.score))
            current = current.next
        return result

    def __repr__(self) -> str:
        """String representation for debugging"""
        nodes = []
        current = self.head
        while current:
            nodes.append(f"{current.username}:{current.score}")
            current = current.next
        return " -> ".join(nodes) if nodes else "Empty"