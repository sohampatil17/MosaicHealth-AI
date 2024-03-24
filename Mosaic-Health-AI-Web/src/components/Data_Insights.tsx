import { Button, Card, Typography, Sheet, Chip } from '@mui/joy';
import { Key, useEffect, useState } from 'react';

const importantData = [
    {
        reasoning: "Mentioned *muscle pain* which can be caused by vitamin d deficiency",
        category: "Time In Daylight",
        data1_time: "6 month",
        data1_type: "mean",
        data2_time: "3 month",
        data2_type: "trend"
    },
    {
        reasoning: "Shortness of breath might indicate oxygen issues",
        category: "Oxygen Saturation",
        data1_time: "1 week",
        data1_type: "min",
        data2_time: "6 month",
        data2_type: "mean"
    },
];

export default function DataInsights() {
    const [appleHealthData, setAppleHealthData] = useState<any | null>(null);
    const [enrichedData, setEnrichedData] = useState<any | null>([]);
    const [selectedData, setSelectedData] = useState<string[]>([]);

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

    // Function to handle chip clicks
    const handleChipClick = (chipData: { data1_time: any; data1_type: any; data1_value: any; unit: any; }) => {
        const chipString = `${chipData.data1_time} ${chipData.data1_type}: ${chipData.data1_value} ${chipData.unit}`;
        if (selectedData.includes(chipString)) {
            setSelectedData(selectedData.filter(data => data !== chipString)); // Remove from selectedData
        } else {
            setSelectedData([...selectedData, chipString]); // Add to selectedData
        }
    };

    return (
        <Card color='primary' sx={{ margin: 2, marginRight: 0, justifyItems: 'top', alignItems: 'center' }}>
            <Typography level='h3'>Data Insights</Typography>
            <Typography> Select data chips to include them in the AI report outline</Typography>
            <Sheet sx={{ width: '100%', height: '54vh', overflowY: 'auto' }}>
                {enrichedData && enrichedData.map((data: any, index: any) => (
                    <Card key={index} sx={{ width: '100%', marginTop: 0, marginBottom: 2 }}>
                        <Typography level='h3'>{data.category}</Typography>
                        <Sheet sx={{ alignItems: 'center', overflowX: 'auto', flexWrap: 'nowrap' }}>
                            {/* Make Chips clickable and toggle variant based on selection */}
                            <Chip
                                size="lg"
                                variant={selectedData.includes(`${data.data1_time} ${data.data1_type}: ${data.data1_value} ${data.unit}`) ? 'solid' : 'soft'}
                                color='primary'
                                sx={{ marginRight: 1, marginBottom: 1 }}
                                onClick={() => handleChipClick(data)}
                            >
                                {data.data1_time} {data.data1_type}: {data.data1_value} {data.unit}
                            </Chip>
                            <Chip
                                size="lg"
                                variant={selectedData.includes(`${data.data2_time} ${data.data2_type}: ${data.data2_value} ${data.unit}`) ? 'solid' : 'soft'}
                                color='primary'
                                sx={{ marginRight: 0, marginBottom: 1 }}
                                onClick={() => handleChipClick({ ...data, data1_time: data.data2_time, data1_type: data.data2_type, data1_value: data.data2_value })} // Reuse handleChipClick for the second chip by adjusting the properties
                            >
                                {data.data2_time} {data.data2_type}: {data.data2_value} {data.unit}
                            </Chip>
                        </Sheet>
                        <Typography sx={{ marginTop: 0 }}>{data.reasoning}</Typography>
                    </Card>
                ))}
            </Sheet>
            <Button size='lg'>
                ✨ Generate Outline From Selected Data and Transcript ✨
            </Button>
        </Card>
    );
}
