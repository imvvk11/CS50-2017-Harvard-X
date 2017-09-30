def credit_card_validity():
    result1 = 0
    result2 = 0
    evaluate = 0
    total = " "
    card_num = str(input("Enter your card no: " ))
    try:
        if len(card_num) == 15:
            for i in range(1,len(card_num),2):

                if int(card_num[i]) * 2 > 9:
                    evaluate += (1 + (int(card_num[i])*2-10))

                else:
                    result1 += int(card_num[i])*2

            for k in range(0,len(card_num),2):
                    result2 = result2 + int(card_num[k])


            total += str(result1 + result2 + evaluate)

            if total[-1] == "0":
                print ("AMEX")
            else:
                print ("Invalid")
        else:
            print("Invalid card!")



    except ValueError:
        print("Invalid!")



credit_card_validity()
