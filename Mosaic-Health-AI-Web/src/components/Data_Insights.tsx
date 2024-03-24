import { Card, Typography } from '@mui/joy';
import { Key, useEffect, useState } from 'react';

// todo: implement an AI model to predict what data is actually important
const importantData = [
    {
        reasoning: "Patient mentioned *muscle pain* which can be caused by *vitamin d deficiency*",
        category: "TimeInDaylight",
        data1_time: "6_month",
        data1_type: "mean",
        data2_time: "3_month",
        data2_type: "trend"
    },
    {
        reasoning: "second example important data point",
        category: "RespiratoryRate",
        data1_time: "1_week",
        data1_type: "trend",
        data2_time: "6_month",
        data2_type: "min"
    },
];

export default function DataInsights() {
    const [appleHealthData, setAppleHealthData] = useState<any | null>(null);
    const [enrichedData, setEnrichedData] = useState<any | null>([]);

    // load JSON data when component mounts 
    useEffect(() => {
        fetch('/assets/sample_output.json')
            .then(response => response.json())
            .then(data => setAppleHealthData(data))
            .catch(error => console.error('Error fetching data: ', error));
    }, []);

    // Extract data when either the input health data changes, or the 'important information' object updates
    useEffect(() => {
        if (appleHealthData) {
            const enrichedData = importantData.map(dataPoint => {
                const data1_value = appleHealthData.data[dataPoint.category]?.[dataPoint.data1_time]?.[dataPoint.data1_type];
                const data2_value = appleHealthData.data[dataPoint.category]?.[dataPoint.data2_time]?.[dataPoint.data2_type];

                // Return a new object that includes the extracted values
                return {
                    ...dataPoint, // Spread the existing dataPoint properties
                    data1_value,  // Add the new data1_value
                    data2_value   // Add the new data2_value
                };
            });

            setEnrichedData(enrichedData);
        }
    }, [appleHealthData, importantData]);

    return (
        <Card color='primary' sx={{ margin: 2, justifyContent: 'center', width: '60%' }}>
            <Typography> Data Insights </Typography>
            {enrichedData && enrichedData.map((data: any, index: Key | null | undefined) => (
                <div key={index}>
                    <div>{data.category}</div>
                    <div>{data.data1_time} {data.data1_type}: {data.data1_value}</div>
                    <div>{data.data2_time} {data.data2_type}: {data.data2_value}</div>
                </div>
            ))}
        </Card>
    );
}
