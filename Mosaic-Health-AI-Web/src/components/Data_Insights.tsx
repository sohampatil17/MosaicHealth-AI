import { Button, Card, Typography, Sheet, Chip } from '@mui/joy';
import { Key, useEffect, useState } from 'react';

// todo: add +/- % to trend data
// todo: rounding

// todo: implement an AI model to predict what data is actually important
const importantData = [
    {
        reasoning: "Mentioned *muscle pain* which can be caused by *vitamin d deficiency*",
        category: "Time In Daylight",
        data1_time: "6 month",
        data1_type: "mean",
        data2_time: "3 month",
        data2_type: "trend"
    },
    {
        reasoning: "Waking up in the night might indicate ",
        category: "Sleep Awake Time",
        data1_time: "1 week",
        data1_type: "trend",
        data2_time: "6 month",
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
                const unit = appleHealthData.data[dataPoint.category]?.unit;
                const data1_value = appleHealthData.data[dataPoint.category]?.[dataPoint.data1_time]?.[dataPoint.data1_type];
                const data2_value = appleHealthData.data[dataPoint.category]?.[dataPoint.data2_time]?.[dataPoint.data2_type];

                // Return a new object that includes the extracted values
                return {
                    ...dataPoint, // Spread the existing dataPoint properties
                    unit,
                    data1_value,  // Add the new data1_value
                    data2_value   // Add the new data2_value
                };
            });

            setEnrichedData(enrichedData);
        }
    }, [appleHealthData, importantData]);

    return (
        <Card color='primary' sx={{ margin: 2, justifyItems: 'top', alignItems: 'center', width: '60%' }}>
            <Typography level='h2'>Data Insights</Typography>
            <Sheet sx={{ width: '100%', height: 'calc(90vh - 120px)', overflowY: 'auto' }}>
                {enrichedData && enrichedData.map((data: any, index: Key | null | undefined) => (
                    <Card key={index} sx={{ width: '100%', marginTop: 2, marginBottom: 2 }}>
                        <Sheet sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', overflowX: 'auto', flexWrap: 'nowrap' }}>
                            <Typography level='h3'>{data.category}</Typography>
                            <Chip size="lg" variant="soft" color='primary'>{data.data1_time} {data.data1_type}: {data.data1_value} {data.unit}</Chip>
                            <Chip size="lg" variant="soft" color='primary'>{data.data2_time} {data.data2_type}: {data.data2_value}</Chip>
                        </Sheet>
                        <Typography>{data.reasoning}</Typography>
                    </Card>
                ))
                }
            </Sheet >
            <Button>✨Get AI Recommended Data✨</Button>
        </Card >
    );
}
