class CollectMethod:
    __collect_dict = {}
    __collect_number = 0

    @classmethod
    def dict_collect(cls, str):
        if str in cls.__collect_dict:
            cls.__collect_dict[str] += 1
        else:
            cls.__collect_dict[str] = 1
        
    @classmethod
    def double_dict_collect(cls, k1, k2):
        if (k1, k2) in cls.__collect_dict:
            cls.__collect_dict[k1, k2] += 1
        else:
            cls.__collect_dict[k1, k2] = 1
    
    @classmethod
    def number_collect(cls, number):
        cls.__collect_number += number

    @classmethod
    def return_collect(self):
        if len(self.__collect_dict) > 0:
            sorted_dict = sorted(self.__collect_dict.items(), key=lambda x: x[1], reverse=True)
            return sorted_dict
        return self.__collect_number
    
    @classmethod
    def clear_collect(cls):
        cls.__collect_dict.clear()
        cls.__collect_number = 0