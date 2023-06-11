import React, { useState } from "react";
import axios from 'axios';
import styles from "../styles/Spinner.module.css";

export default function NotionChat() {
  const [notionToken, setNotionToken] = useState("");
  const [databaseId, setDatabaseId] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [databaseCreated, setDatabaseCreated] = useState(false);
  const [isLoading, setLoading] = useState(false);
  const [isSubmitting, setSubmitting] = useState(false);
  
  const API_URL = 'https://f800-2600-8801-a800-f300-6995-4fba-56db-e196.ngrok-free.app';

  const handleNotionIntegration = async () => {
    try {
      setLoading(true);
      const response = await axios.post(`${API_URL}/create_db`, {
        notion_token: notionToken,
        database_id: databaseId
      });
      if (response.data.message) {
        alert(response.data.message);
        setDatabaseCreated(true);
      } else {
        throw new Error("Failed to create database");
      }
    } catch (error) {
      console.error("An error occurred while creating the database:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleQuestionSubmission = async () => {
    try {
      setSubmitting(true);
      const response = await axios.post(`${API_URL}/get_response`, {
        notion_token: notionToken,
        database_id: databaseId,
        question: question
      });

      if (response.data.response) {
        setAnswer(response.data.response);
      } else {
        throw new Error("Failed to get response");
      }
    } catch (error) {
      console.error("An error occurred while fetching the response:", error);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={{textAlign: 'center'}}>
      <div style={{marginBottom: '1rem'}}>
        <label>Notion Token:</label><br/>
        <input 
          type="text"
          onChange={(e) => setNotionToken(e.target.value)} 
          style={{width: '300px', margin: '0 auto'}}
        />
      </div>

      <div style={{marginBottom: '1rem'}}>
        <label>Database ID:</label><br/>
        <input 
          type="text"
          onChange={(e) => setDatabaseId(e.target.value)}
          style={{width: '300px', margin: '0 auto'}} 
        />
      </div>

      <div>
        <button onClick={handleNotionIntegration} disabled={isLoading}>
          {isLoading ? (
            <div className={styles.spinner}></div>
          ) : (
            "Create Database"
          )}
        </button>
      </div>

      {databaseCreated && (
        <>
          <hr />

          <div style={{marginBottom: '1rem'}}>
            <label>Your Question:</label><br/>
            <input 
              type="text"
              onChange={(e) => setQuestion(e.target.value)}
              style={{width: '300px', margin: '0 auto'}} 
            />
          </div>

          <div>
            <button onClick={handleQuestionSubmission} disabled={isSubmitting}>
              {isSubmitting ? (
                <div className={styles.spinner}></div>
              ) : (
                "Submit Question"
              )}
            </button>
          </div>

          <hr />

          <div>
            <h3>Answer:</h3>
            <p>{answer}</p>
          </div>
        </>
      )}
    </div>
  );

}