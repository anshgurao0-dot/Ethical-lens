import axios from 'axios';

// Replace with your machine's local IP if testing on a real device
const API_URL = 'http://192.168.29.103:8095'; // Port 8095

export interface UserProfile {
    user_id: string;
    health_profile: {
        allergens: string[];
        conditions: string[];
        age?: number;
        dietary_restrictions: string[];
    };
    value_profile: {
        weights: Record<string, number>;
    };
}

export interface ProductAnalysis {
    product_id: string;
    product_name: string;
    overall_score: number;
    overall_status: 'RED' | 'YELLOW' | 'GREEN';
    agent_verdicts: AgentVerdict[];
}

export interface AgentVerdict {
    agent_name: string;
    score: number;
    status: 'RED' | 'YELLOW' | 'GREEN';
    reasoning: string;
    details: any;
}

export const analyzeProduct = async (barcode: string, userProfile: UserProfile): Promise<ProductAnalysis | null> => {
    try {
        const response = await axios.post(`${API_URL}/analyze`, {
            barcode,
            user_profile: userProfile,
        });
        return response.data;
    } catch (error) {
        console.error('Error analyzing product:', error);
        return null;
    }
};
