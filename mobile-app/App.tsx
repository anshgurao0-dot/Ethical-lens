import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import ScannerScreen from './src/screens/ScannerScreen';
import ProductDetailsScreen from './src/screens/ProductDetailsScreen';
import ImpactGardenScreen from './src/screens/ImpactGardenScreen';

const Stack = createNativeStackNavigator();

export default function App() {
    return (
        <NavigationContainer>
            <Stack.Navigator>
                <Stack.Screen name="Scanner" component={ScannerScreen} options={{ headerShown: false }} />
                <Stack.Screen name="ProductDetails" component={ProductDetailsScreen} options={{ title: 'Analysis Results' }} />
                <Stack.Screen name="ImpactGarden" component={ImpactGardenScreen} options={{ title: 'My Garden', headerShown: false }} />
            </Stack.Navigator>
        </NavigationContainer>
    );
}
