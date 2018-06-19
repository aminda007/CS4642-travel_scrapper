next_page_list=['/watch?v=OBbb8D7qN_Mblacklistinstagram', '/watch?v=OBbb8D7qN_Mblacklistinstagram']
for page in next_page_list:
    # print(page)
    black_list = ['youtube', 'watch?v', 'twitter', 'instagram', 'wikipedia', 'facebook']
    if not any(substring in page for substring in black_list):
        print("ADDING: " + page)


# black_list = ['youtube', 'watch?v', 'twitter', 'instagram', 'wikipedia', 'facebook']
# string='/=OBbb8D7qN_Mblacklisttwitter'
# f = any(substring in string for substring in black_list)
# print(f)