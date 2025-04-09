import base64
import os
import pandas as pd

def encode_image(image_path):
    """Encode the image to base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None
    except Exception as e:  # Added general exception handling
        print(f"Error: {e}")
        return None
    
personal_infromation_description = """ 
        "Analyse the input text which is the ocr response of a bank statement image \n"
        "First, extract the personal information of the account holder from the text :  \n"
        "- **Account Number** \n"
        "- **Name** \n"
        "- **Address of the account holder** \n"
        "- **Phone Number of the account holder** \n"
        "- **Email of the account** \n"
        "- **Bank Name** \n"
        "- **Branch Name** \n"
"""

transaction_description = """  
        "Then, extract the credit and debit transactions along with the transaction number from the bank statement and output in the following manner : \n"
        "- **Account number** \n"
        "- **Transaction date** \n"
        "- **Description/Particulars** \n"
        "- **UTR No/Sender** \n"
        "- **Amount (INR)** \n"
        "- **Credit/Debit** \n"
        "- **Balance (INR)** \n"

        "NOTE : For the description/particular part, if either of the keyword in not there in the text then look for the the word which might mean the same thing based on the context of the input text"
    """

expected_output = """ 
        "First, the extracted personal information should be printed in the console."
        "Print ONLY the extracted details in the console in the format specified below in a single line.\n"
        "{'Account number': '<account_number>', 'Name': '<name>', 'Address': '<address>', 'Phone Number': '<phone_number>', 'Email': '<email>', 'Bank Name': '<bank_name>', 'Branch Name': '<branch_name>'}"
        "If any information is missing, keep the value as an empty string.\n"
        "Extract only the main personal details required from the bank statement.\n"
        "Try to limit down to the necessary information.\n"
       
        "Second, the extracted transaction details should be printed in the console."
        "Print ONLY the extracted details in the console in the format specified below in a single line.\n"
        "{'Account number': '<account_number>', 'Transaction date': '<transaction_date>', 'Description/Particulars': '<description>', 'UTR No/Sender': '<utr_sender>', 'Amount (INR)': '<amount>', 'Credit/Debit': '<credit_debit>', 'Balance (INR)': '<balance>'}"
        "If there are multiple transactions, separate them by newlines.\n"
        "Extract only the main details required for each transaction from the bank statement.\n"
        "Try to limit down to the necessary information.\n"
        "EXAMPLE: \n "
        "{'Account number': 'XXXXXX1234', 'Name': 'John Doe', 'Address': '123 Main Street, City, State, ZIP', 'Phone Number': '+91-1234567890', 'Email': 'john.doe@example.com', 'Bank Name': 'ABC Bank', 'Branch Name': 'Downtown Branch'}\n"
        "{'Account number': 'XXXXXX1234', 'Transaction date': '01-01-2023', 'Description/Particulars': 'ATM Withdrawal', 'UTR No/Sender': 'ATM12345', 'Amount (INR)': '5000.00', 'Credit/Debit': 'Debit', 'Balance (INR)': '10000.00'}\n"
        "{'Account number': 'XXXXXX1234', 'Transaction date': '03-02-2020', 'Description/Particulars': 'ATM Withdrawal', 'UTR No/Sender': 'ATM12357', 'Amount (INR)': '50.00', 'Credit/Debit': 'Debit', 'Balance (INR)': '1000.00'}\n"
        
        "NOTE : DON'T include pre-sentences like 'The info.csv now contains the following details -' etc. in the final output. \n"
        "NOTE :DON'T include any extra characters like ``` or any other extra words in the final output."
    """

backstory = "You are an expert in analysing financial records and understanding the credit and debit transactions"
goal = "Extract the credit and debit transactions from the bank statement along with the personal information of the account holder"

# def push_into_csv(final_output):
#     personal_info = final_output.split('\n')[0]

#     transaction_info = final_output.split('\n')[2:]

#     personal_file_exists = os.path.exists("personal_info.csv")
#     result_df_personal = pd.DataFrame([eval(str(personal_info))],columns=eval(str(personal_info)).keys())
#     result_df_personal.to_csv("personal_info.csv",mode='a', index=False, header=not personal_file_exists)

#     for transaction in final_output.split('\n')[2:]:
#         transaction_file_exists = os.path.exists("transactions.csv")
#         result_df_transc = pd.DataFrame([eval(str(transaction))],columns=eval(str(transaction)).keys())
#         result_df_transc.to_csv("transaction.csv",mode='a', index=False, header=not transaction_file_exists)

#     return "pushed all records"

def push_into_csv(final_output,image_name):
    import pandas as pd
    import os

    personal_info = final_output.split('\n')[0]
    transaction_info = final_output.split('\n')[2:]

    # Save personal info
    personal_file_exists = os.path.exists(f"personal_info_{image_name}.csv")
    try:
        personal_data = eval(personal_info)
        result_df_personal = pd.DataFrame([personal_data], columns=personal_data.keys())
        result_df_personal.to_csv(f"personal_info_{image_name}.csv", mode='a', index=False, header=not personal_file_exists)
    except Exception as e:
        print(f"Error in personal_info parsing: {e}")

    # Save transaction info
    transaction_file_exists = os.path.exists(f"transactions_{image_name}.csv")
    transaction_data = []
    for transaction in transaction_info:
        try:
            # Fix data parsing by checking for valid dictionary format
            if transaction.strip():
                transaction_data.append(eval(transaction))
        except Exception as e:
            print(f"Error in transaction parsing: {e}")

    if transaction_data:
        result_df_transc = pd.DataFrame(transaction_data)
        result_df_transc.to_csv(f"transactions_{image_name}.csv", mode='a', index=False, header=not transaction_file_exists)

    return "Pushed all records"


def note_token_usage(image_name,usage_output):
    with open("token_usage_ds.txt","a") as f:
        f.write(f"{image_name} : {usage_output}\n")
    return f"pushed token usage for {image_name}"

def write_pixtral_response(response_dir,response,image_name):
    with open(os.path.join(response_dir,image_name +'.txt'),"w") as f:
        f.write(response)
    return f"pushed response for {image_name}"

def write_response(pixtral_resp_sir,ds_resp_dir,pixtral_resp,ds_resp,image_name):
    write_pixtral_response(pixtral_resp_sir,pixtral_resp,image_name)
    with open(os.path.join(ds_resp_dir,image_name +'.txt'),"w") as f:
        f.write(ds_resp)
    return f"pushed response for {image_name}"