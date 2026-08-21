# AgriPredict

Predict. Understand. Plan. Grow.

AgriPredict is an AI-powered agricultural decision-support platform that predicts crop yield from historical, environmental, and soil data.

## Team

- Anshul Dixit — AI/ML & Data
- Sidharth Kumar — Backend
- Shivam Gupta — Frontend

## Project

Built by Team ByteForge for Prasunethon 2.0.


## 📊 Data Engineering & Architecture

**Data Fusion Pipeline**
Our original yield dataset had 55 crops, but to ensure high accuracy for our ML model, we performed a strict inner-join with our IoT sensor dataset. We dropped crops that lacked baseline NPK and pH profiles, resulting in a highly validated, complete dataset for Rice, Wheat, Maize, Sugarcane, and Potato. 

*Note: In the future, as we get more sensor data for other crops, our pipeline will automatically scale to include them.*