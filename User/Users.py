class Node:
    def __init__(self, username, score):
        self.username = username
        self.score = score
        self.next = None

class LeaderboardLinkedList:
    def __init__(self):
        self.head = None 

    def insert_sorted(self, username, score):
        new_node = Node(username, score)

        if self.head is None or score > self.head.score:
            new_node.next = self.head
            self.head = new_node
            return

        current = self.head
        while current.next and current.next.score >= score:
            current = current.next

        new_node.next = current.next
        current.next = new_node

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append((current.username, current.score))
            current = current.next
        return result
