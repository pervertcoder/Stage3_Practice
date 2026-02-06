import datetime

def time_process() -> str:
    first_step = str(datetime.datetime.today()).split(" ")
    second_step = first_step[0].replace("-", "")
    third_step = first_step[1].replace(":", "")
    forth_step = third_step.replace(".", "")
    ans = second_step + forth_step
    return ans

def file_name_process(file_name:str, time_block:str) -> str:
    vice = file_name[-4:]
    file_name_deal = file_name[0:-4]
    ans = file_name_deal + time_block + vice
    return ans