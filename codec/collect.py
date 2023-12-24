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
    def double_dict_collect(cls, k1, k2):
        if (k1, k2) in cls.collect_dict:
            cls.collect_dict[k1, k2] += 1
        else:
            cls.collect_dict[k1, k2] = 1
    
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
    
    @classmethod
    def return_double_collect(self):
        for k1, k2 in self.collect_dict:
            print(k1, k2, self.collect_dict[k1, k2])