import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { ProductAnalysis, AgentVerdict } from '../services/api';

export default function ProductDetailsScreen({ route }: any) {
    const { product } = route.params as { product: ProductAnalysis };

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'RED': return '#ffcccc';
            case 'YELLOW': return '#ffffcc';
            case 'GREEN': return '#ccffcc';
            default: return '#eee';
        }
    };

    return (
        <ScrollView style={styles.container}>
            <View style={[styles.header, { backgroundColor: getStatusColor(product.overall_status) }]}>
                <Text style={styles.productName}>{product.product_name}</Text>
                <Text style={styles.score}>Score: {product.overall_score.toFixed(1)}</Text>
                <Text style={styles.status}>{product.overall_status}</Text>
            </View>

            <Text style={styles.sectionTitle}>Agent Verdicts</Text>

            {product.agent_verdicts.map((verdict, index) => (
                <View key={index} style={[styles.card, { borderLeftColor: getStatusColor(verdict.status) }]}>
                    <Text style={styles.agentName}>{verdict.agent_name}</Text>
                    <Text style={styles.reasoning}>{verdict.reasoning}</Text>
                    <Text style={styles.details}>Status: {verdict.status}</Text>
                </View>
            ))}
        </ScrollView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
    },
    header: {
        padding: 20,
        alignItems: 'center',
        borderBottomWidth: 1,
        borderBottomColor: '#ccc',
    },
    productName: {
        fontSize: 24,
        fontWeight: 'bold',
    },
    score: {
        fontSize: 18,
        marginTop: 5,
    },
    status: {
        fontSize: 16,
        fontWeight: 'bold',
        marginTop: 5,
    },
    sectionTitle: {
        fontSize: 20,
        fontWeight: 'bold',
        margin: 15,
    },
    card: {
        marginHorizontal: 15,
        marginBottom: 10,
        padding: 15,
        backgroundColor: '#f9f9f9',
        borderRadius: 8,
        borderLeftWidth: 5,
        elevation: 2,
    },
    agentName: {
        fontSize: 18,
        fontWeight: 'bold',
        marginBottom: 5,
    },
    reasoning: {
        fontSize: 14,
        marginBottom: 5,
    },
    details: {
        fontSize: 12,
        color: '#666',
    },
});
