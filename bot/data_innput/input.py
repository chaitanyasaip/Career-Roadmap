import requests
from bs4 import BeautifulSoup

url = "https://boards.greenhouse.io/enveritas/jobs/4001717008"

def user_input(url):
    # Send a GET request to the URL
    input
    response = requests.get(url)

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the job description content
    job_title = soup.find("h1", {"class": "app-title"})

    company_name = soup.find("span",{"class": "company-name"})

    job_location = soup.find("div", {"class": "location"})

    job_description = soup.find("div", {"id": "content"})

    '''
    # Print the job description
    if job_description:
        print("Job Title: "+job_title.get_text()+"\n"+"Company: "+company_name.get_text().strip().split("at ")[1]+"\n"+"Job Location: "+job_location.get_text().strip()+"\n"+"Job Description: \n"+job_description.get_text().strip())
    else:
        print("Job description not found.")
    '''

    # Open a text file in write mode
    with open('job_details.txt', 'w', encoding='utf-8') as file:
        # Write the job details to the file
        file.write("Job Title: " + job_title.get_text() + "\n")
        file.write("Company: " + company_name.get_text().strip().split("at ")[1] + "\n")
        file.write("Job Location: " + job_location.get_text().strip() + "\n")
        file.write("Job Description: \n" + job_description.get_text().strip() + "\n")