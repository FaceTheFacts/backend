from src.api.utils.error import check_entity_not_found
from fastapi import HTTPException

def test_check_entity_not_found():
    def pass_None_test():
        try:
            check_entity_not_found(None, "Entity")
            assert False, "check_entity_not_found does not throw HTTPException when None is passed as entity"
        except HTTPException:
            assert True


    def pass_empty_list_test():
        try:
            check_entity_not_found([], "Entity")
            assert False, "check_entity_not_found does not throw HTTPException when empty list is passed as entity"
        except HTTPException:
            assert True
    pass_None_test()
    pass_empty_list_test()