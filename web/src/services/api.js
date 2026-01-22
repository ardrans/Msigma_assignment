/**
 * API Service Layer
 * Centralized API calls for the batch processor frontend
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

/**
 * Create a new record
 * @param {Object} data - Record data (name, email, phone_number, link, dob)
 * @returns {Promise<Object>} - API response
 */
export const createRecord = async (data) => {
    const response = await fetch(`${API_BASE_URL}/records/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.message || 'Failed to create record');
    }

    return result;
};

/**
 * Get all records with SUCCESS status
 * @returns {Promise<Object>} - API response with records array
 */
export const getSuccessRecords = async () => {
    const response = await fetch(`${API_BASE_URL}/records/success/`);

    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.message || 'Failed to fetch records');
    }

    return result;
};
