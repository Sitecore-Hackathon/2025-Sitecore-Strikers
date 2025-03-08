![Hackathon Logo](docs/images/hackathon.png?raw=true "Hackathon Logo")
# Sitecore Hackathon 2025

## Team name
⟹ Sitecore Strikers

## Category
⟹  Sitecore Authoring API with AI Integration.

## Description
 
Problem Statement:
In today’s fast-paced digital world, businesses must stay updated with real-time news to make informed decisions. However, challenges such as news authenticity, relevant categorization, and sentiment analysis make it difficult to derive meaningful insights from vast amounts of data.

    •	Misinformation & Fake News: With the rise of misinformation, businesses risk making decisions based on unreliable sources.
    •	Information Overload: Manually filtering and categorizing news relevant to the business is time-consuming and inefficient.
    •	Understanding Sentiment: Businesses need to gauge the sentiment of news articles (positive, negative, or neutral) to assess potential impacts.

This solution ensures businesses receive only relevant, credible, and sentiment-aware news, eliminating the manual effort required for news filtering and analysis.

Here is the attached document -
[ModuleUseCase](docs/Automating-News-Feed-Integration-into-Sitecore-XMC-with-AI.docx)

## Video link
⟹ Provide a video highlighing your Hackathon module submission and provide a link to the video. You can use any video hosting, file share or even upload the video to this repository. _Just remember to update the link below_

⟹ [SitecoreStrikerHackathonVideo](https://www.youtube.com/watch?v=KgDBDZd3tWw)

## Pre-requisites and Dependencies

    > An active XM Cloud instance with the Authoring API enabled. 
    > A Client ID and Client Secret readily available to generate an access token for using the Authoring API's mutation queries. 
    > The GraphQL Authoring API URL should be accessible, e.g., https://YOUR-XMC-DOMAIN/sitecore/api/authoring/graphql/v1 . 
    > A News API service for proof-of-concept purposes. We have used this API with an API key: https://newsapi.org/v2/top-headlines?country=us&apiKey=095392c11b2945928e1d34da0db48c10 . 
    > An active Azure subscription to create and host the Azure Function for executing the given Python script. 
    > Python should be installed on your local machine. Testing was conducted on version 3.12.6.


## Installation instructions
1. Clone the repository in your local environment from GitHub.
2. Open the repository in VS Code and if needed install the Python extension. 
3. Open the terminal and select Git Bash and navigate to the directory “2025-Sitecore-Strikers/src/newsfeed”.
4. Run the following command:  pip install -r requirements.txt
5. Update the following variables in the authoring.py file.
    GRAPHQL_Authoring_URL
    ACCESS_TOKEN 
6. To generate the ACCESS_TOKEN run the below command in the command prompt using your Client ID and Client Secret.
    cmd /c curl --request POST --url "https://auth.sitecorecloud.io/oauth/token" --header "content-type: application/x-www-form-urlencoded" --data audience=https://api.sitecorecloud.io --data grant_type=client_credentials --data client_id={{Client ID}} --data client_secret={{Client Secret}}
7. Now login to your XMC instance and install the following Sitecore package.
    [SitecoreHackathonPackage](src/NewsFeed/SitecoreHackathonPackage2025.zip)
8. Now go back to your VS code and run the following command it should push the news articles including AI analysis results in the XMC instance in Home/News folder. 
    python authoring.py

Note – Please refer to the document attached for the detailed steps. Please use headset for better audio video quality. Thank you
