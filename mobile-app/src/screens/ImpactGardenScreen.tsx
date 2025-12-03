import React from 'react';
import { View, Text, StyleSheet, Image, ScrollView, TouchableOpacity } from 'react-native';

export default function ImpactGardenScreen({ navigation }: any) {
    // Mock Data: In a real app, this would come from the UserProfile/Backend
    const stats = {
        treesPlanted: 12,
        carbonSaved: "45kg",
        plasticAvoided: "120 items",
        level: "Eco-Warrior"
    };

    return (
        <ScrollView contentContainerStyle={styles.container}>
            <View style={styles.header}>
                <Text style={styles.title}>My Impact Garden</Text>
                <Text style={styles.subtitle}>Level: {stats.level}</Text>
            </View>

            <View style={styles.gardenContainer}>
                {/* Placeholder for a dynamic tree visualization */}
                <View style={styles.treePlaceholder}>
                    <Text style={styles.treeEmoji}>🌳</Text>
                    <Text style={styles.treeCount}>{stats.treesPlanted}</Text>
                    <Text style={styles.treeLabel}>Trees Planted</Text>
                </View>
            </View>

            <View style={styles.statsGrid}>
                <View style={styles.statCard}>
                    <Text style={styles.statValue}>{stats.carbonSaved}</Text>
                    <Text style={styles.statLabel}>CO2e Saved</Text>
                </View>
                <View style={styles.statCard}>
                    <Text style={styles.statValue}>{stats.plasticAvoided}</Text>
                    <Text style={styles.statLabel}>Plastic Avoided</Text>
                </View>
            </View>

            <View style={styles.achievementsContainer}>
                <Text style={styles.sectionTitle}>Recent Achievements</Text>
                <View style={styles.achievementRow}>
                    <Text style={styles.achievementIcon}>🏆</Text>
                    <View>
                        <Text style={styles.achievementTitle}>Palm Oil Free Streak</Text>
                        <Text style={styles.achievementDesc}>Scanned 5 products without Palm Oil.</Text>
                    </View>
                </View>
                <View style={styles.achievementRow}>
                    <Text style={styles.achievementIcon}>♻️</Text>
                    <View>
                        <Text style={styles.achievementTitle}>Recycling Pro</Text>
                        <Text style={styles.achievementDesc}>Checked recycling info 10 times.</Text>
                    </View>
                </View>
            </View>

            <TouchableOpacity style={styles.backButton} onPress={() => navigation.goBack()}>
                <Text style={styles.buttonText}>Back to Scanner</Text>
            </TouchableOpacity>
        </ScrollView>
    );
}

const styles = StyleSheet.create({
    container: {
        flexGrow: 1,
        backgroundColor: '#E8F5E9', // Light Green
        padding: 20,
        alignItems: 'center',
    },
    header: {
        marginTop: 40,
        marginBottom: 20,
        alignItems: 'center',
    },
    title: {
        fontSize: 28,
        fontWeight: 'bold',
        color: '#2E7D32',
    },
    subtitle: {
        fontSize: 18,
        color: '#4CAF50',
        marginTop: 5,
    },
    gardenContainer: {
        width: '100%',
        height: 200,
        backgroundColor: '#C8E6C9',
        borderRadius: 20,
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: 20,
        elevation: 5,
    },
    treePlaceholder: {
        alignItems: 'center',
    },
    treeEmoji: {
        fontSize: 80,
    },
    treeCount: {
        fontSize: 36,
        fontWeight: 'bold',
        color: '#1B5E20',
    },
    treeLabel: {
        fontSize: 16,
        color: '#388E3C',
    },
    statsGrid: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        width: '100%',
        marginBottom: 20,
    },
    statCard: {
        backgroundColor: 'white',
        width: '48%',
        padding: 20,
        borderRadius: 15,
        alignItems: 'center',
        elevation: 3,
    },
    statValue: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#2E7D32',
    },
    statLabel: {
        fontSize: 14,
        color: '#757575',
    },
    achievementsContainer: {
        width: '100%',
        backgroundColor: 'white',
        borderRadius: 15,
        padding: 20,
        elevation: 3,
        marginBottom: 20,
    },
    sectionTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        marginBottom: 15,
        color: '#424242',
    },
    achievementRow: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 15,
    },
    achievementIcon: {
        fontSize: 24,
        marginRight: 15,
    },
    achievementTitle: {
        fontSize: 16,
        fontWeight: 'bold',
        color: '#212121',
    },
    achievementDesc: {
        fontSize: 12,
        color: '#757575',
    },
    backButton: {
        backgroundColor: '#2E7D32',
        paddingVertical: 15,
        paddingHorizontal: 40,
        borderRadius: 30,
    },
    buttonText: {
        color: 'white',
        fontSize: 16,
        fontWeight: 'bold',
    }
});
