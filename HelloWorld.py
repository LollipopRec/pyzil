class HelloworldContract:
    def __init__(self):
        print("init func in contract")

    def recall(self):
        print("recall func in contract")
        return "recall invoke"

    def rank(self):
        print("rank func")
        return "rank invoke"

#if __name__ == '__main__':
#    contract = HelloworldContract()
#    contract.recall()

