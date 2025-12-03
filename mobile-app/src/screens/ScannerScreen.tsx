import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ActivityIndicator, TouchableOpacity } from 'react-native';
import { CameraView, Camera } from 'expo-camera';
import * as Speech from 'expo-speech';
import { analyzeProduct, UserProfile, ProductAnalysis } from '../services/api';

// Mock User Profile for Demo
const DEMO_USER_PROFILE: UserProfile = {
    user_id: "demo_user",
    health_profile: {
        allergens: ["Peanuts", "Gluten"],
        conditions: ["Diabetes"],
        dietary_restrictions: ["Vegan"]
    },
    value_profile: {
        weights: {
            "palm_oil": 1.0,
            "animal_welfare": 0.8,
            "plastic_waste": 0.5
        }
    }
};

export default function ScannerScreen({ navigation }: any) {
    const [hasPermission, setHasPermission] = useState<boolean | null>(null);
    const [scanned, setScanned] = useState(false);
    const [loading, setLoading] = useState(false);
    const [analysis, setAnalysis] = useState<ProductAnalysis | null>(null);

    useEffect(() => {
        const getPermissions = async () => {
            const { status } = await Camera.requestCameraPermissionsAsync();
            setHasPermission(status === 'granted');
        };
        getPermissions();
    }, []);

    const speakVerdict = (analysis: ProductAnalysis) => {
        let text = `Overall status is ${analysis.overall_status}. Score is ${Math.round(analysis.overall_score)}.`;

        const warnings = analysis.agent_verdicts
            .filter(v => v.status !== 'GREEN' && v.reasoning)
            .map(v => `${v.agent_name} says: ${v.reasoning}`);

        if (warnings.length > 0) {
            text += " Warnings found: " + warnings.join(". ");
        } else {
            text += " This product looks good!";
        }

        Speech.speak(text);
    };

    const handleBarCodeScanned = async ({ type, data }: { type: string; data: string }) => {
        setScanned(true);
        setLoading(true);
        console.log(`Bar code with type ${type} and data ${data} has been scanned!`);

        const result = await analyzeProduct(data, DEMO_USER_PROFILE);
        setLoading(false);

        if (result) {
            setAnalysis(result);
            speakVerdict(result);
        } else {
            alert(`Failed to analyze product (Barcode: ${data}). Is the backend running?`);
            setTimeout(() => setScanned(false), 2000);
        }
    };

    const resetScan = () => {
        setScanned(false);
        setAnalysis(null);
        Speech.stop();
    };

    if (hasPermission === null) {
        return <View style={styles.container}><Text>Requesting for camera permission</Text></View>;
    }
    if (hasPermission === false) {
        return <View style={styles.container}><Text>No access to camera</Text></View>;
    }

    return (
        <View style={styles.container}>
            <CameraView
                style={StyleSheet.absoluteFillObject}
                onBarcodeScanned={scanned ? undefined : handleBarCodeScanned}
                barcodeScannerSettings={{
                    barcodeTypes: ["qr", "ean13", "ean8", "upc_a", "upc_e"],
                }}
            />

            {loading && (
                <View style={styles.loadingOverlay}>
                    <ActivityIndicator size="large" color="#00ff00" />
                    <Text style={{ color: 'white', marginTop: 10 }}>Analyzing...</Text>
                </View>
            )}

            {analysis && (
                <View style={styles.arOverlay}>
                    <View style={[styles.statusBubble, { backgroundColor: getStatusColor(analysis.overall_status) }]}>
                        <Text style={styles.scoreText}>{Math.round(analysis.overall_score)}</Text>
                        <Text style={styles.statusText}>{analysis.overall_status}</Text>
                    </View>

                    <View style={styles.infoCard}>
                        <Text style={styles.productName}>{analysis.product_name}</Text>

                        {analysis.agent_verdicts.map((v, i) => {
                            if (v.status !== 'GREEN' && v.reasoning) {
                                return (
                                    <Text key={i} style={styles.warningText}>⚠️ {v.agent_name}: {v.reasoning}</Text>
                                )
                            }
                            return null;
                        })}

                        <View style={styles.buttonGroup}>
                            <TouchableOpacity style={styles.detailsButton} onPress={() => navigation.navigate('ProductDetails', { product: analysis })}>
                                <Text style={styles.buttonText}>Details</Text>
                            </TouchableOpacity>
                            <TouchableOpacity style={styles.speakButton} onPress={() => speakVerdict(analysis)}>
                                <Text style={styles.buttonText}>📢 Speak</Text>
                            </TouchableOpacity>
                            <TouchableOpacity style={styles.scanButton} onPress={resetScan}>
                                <Text style={styles.buttonText}>Scan</Text>
                            </TouchableOpacity>
                        </View>
                    </View>
                </View>
            )}

            {!scanned && !loading && (
                <View style={styles.overlay}>
                    <Text style={styles.scanText}>Scan a Product Barcode</Text>
                    <TouchableOpacity style={styles.gardenButton} onPress={() => navigation.navigate('ImpactGarden')}>
                        <Text style={styles.buttonText}>🌱 View Impact Garden</Text>
                    </TouchableOpacity>
                </View>
            )}
        </View>
    );
}

const getStatusColor = (status: string) => {
    switch (status) {
        case 'GREEN': return '#4CAF50';
        case 'YELLOW': return '#FFC107';
        case 'RED': return '#F44336';
        default: return '#9E9E9E';
    }
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: 'black',
    },
    overlay: {
        position: 'absolute',
        bottom: 50,
        backgroundColor: 'rgba(0,0,0,0.5)',
        padding: 20,
        borderRadius: 10,
        alignItems: 'center',
    },
    scanText: {
        color: 'white',
        fontSize: 18,
    },
    loadingOverlay: {
        ...StyleSheet.absoluteFillObject,
        backgroundColor: 'rgba(0,0,0,0.7)',
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 10,
    },
    arOverlay: {
        ...StyleSheet.absoluteFillObject,
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 20,
    },
    statusBubble: {
        width: 100,
        height: 100,
        borderRadius: 50,
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: 20,
        borderWidth: 4,
        borderColor: 'white',
        elevation: 10,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.25,
        shadowRadius: 3.84,
    },
    scoreText: {
        fontSize: 32,
        fontWeight: 'bold',
        color: 'white',
    },
    statusText: {
        fontSize: 14,
        fontWeight: 'bold',
        color: 'white',
    },
    infoCard: {
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        padding: 20,
        borderRadius: 15,
        width: '85%',
        alignItems: 'center',
    },
    productName: {
        fontSize: 20,
        fontWeight: 'bold',
        marginBottom: 10,
        textAlign: 'center',
    },
    warningText: {
        color: '#D32F2F',
        marginBottom: 5,
        textAlign: 'center',
    },
    buttonGroup: {
        flexDirection: 'row',
        marginTop: 15,
        gap: 10,
    },
    detailsButton: {
        backgroundColor: '#2196F3',
        padding: 10,
        borderRadius: 5,
    },
    speakButton: {
        backgroundColor: '#FF9800',
        padding: 10,
        borderRadius: 5,
    },
    scanButton: {
        backgroundColor: '#757575',
        padding: 10,
        borderRadius: 5,
    },
    buttonText: {
        color: 'white',
        fontWeight: 'bold',
    },
    gardenButton: {
        marginTop: 20,
        backgroundColor: '#4CAF50',
        padding: 10,
        borderRadius: 20,
        paddingHorizontal: 20,
    }
});
