class CollectMethod:
    collect_dict = {}
    collect_number = 0

    @classmethod
    def dict_collect(cls, str):
        if str in cls.collect_dict:
            cls.collect_dict[str] += 1
        else:
            cls.collect_dict[str] = 1
    
    @classmethod
    def number_collect(cls, number):
        cls.collect_number += number

    @classmethod
    def return_collect(self):
        if len(self.collect_dict) > 0:
            sorted_dict = sorted(self.collect_dict.items(), key=lambda x: x[1], reverse=True)
            for key, value in sorted_dict:
                print(key, value)
        print(self.collect_number)