import { Button, Card, Typography, Sheet, Chip, CircularProgress, Box } from '@mui/joy';
import axios from 'axios';
import { useEffect, useState } from 'react';

interface DataInsightsProps {
    importantData: any;
    loadingDataSuggestions: boolean;
    setOutline: React.Dispatch<React.SetStateAction<string>>;
    transcript: string;
}

export default function DataInsights({ importantData, loadingDataSuggestions, setOutline, transcript }: DataInsightsProps) {
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

    // Extract data when either the apple health data changes, or the 'important information' object updates
    useEffect(() => {
        if (appleHealthData) {
            const enrichedData = importantData.map((dataPoint: { category: any; data1_time: string | number; data1_type: string | number; data2_time: string | number; data2_type: string | number; }) => {
                const category = dataPoint.category;
                const unit = appleHealthData.data[dataPoint.category]?.unit;
                const data1_value = appleHealthData.data[dataPoint.category]?.[dataPoint.data1_time]?.[dataPoint.data1_type];
                const data2_value = appleHealthData.data[dataPoint.category]?.[dataPoint.data2_time]?.[dataPoint.data2_type];

                // Return a new object that includes the extracted values
                return {
                    ...dataPoint, // Spread the existing dataPoint properties
                    unit,
                    category,
                    data1_value,  // Add the new data1_value
                    data2_value   // Add the new data2_value
                };
            });

            setEnrichedData(enrichedData);
        }
    }, [appleHealthData, importantData]);

    // Function to handle chip clicks
    const handleChipClick = (chipData: { data1_time: any; data1_type: any; data1_value: any; unit: any; category: any; }) => {
        const chipString = `${chipData.category} ${chipData.data1_time} ${chipData.data1_type}: ${chipData.data1_value} ${chipData.unit}`;
        if (selectedData.includes(chipString)) {
            setSelectedData(selectedData.filter(data => data !== chipString)); // Remove from selectedData
        } else {
            setSelectedData([...selectedData, chipString]); // Add to selectedData
        }
    };

    // Function to handle generating the initial report
    const handleOutlineGenerator = async () => {
        setOutline("AI magic is happening ... this should only take a few seconds")
        // Combine the transcript and the selected data into a single string
        const combinedData = `${transcript} Selected Data: ${selectedData.join(', ')}`;

        try {
            // Make a POST request to your endpoint with the combined data
            const response = await axios.post('http://127.0.0.1:5000/create_report', { combinedData });

            // Assuming the response contains the generated outline in the 'data' property
            console.log(response);
            const generatedOutline = response.data.result;

            // Update the outline state with the generated outline
            setOutline(generatedOutline);
        } catch (error) {
            console.error('Error generating outline:', error);
            // Optionally, update the outline state to indicate an error
            setOutline('Error generating outline. Please try again.');
        }
    };


    return (
        <Card color='primary' sx={{ marginTop: 2, justifyItems: 'top', alignItems: 'center', flexGrow: 1, display: 'flex' }}>
            <Typography level='h3'>Data Insights</Typography>

            {loadingDataSuggestions ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flexGrow: 1 }}>
                    <CircularProgress />
                </Box>
            ) : (
                <Sheet sx={{ width: '100%', overflowY: 'auto', flexGrow: 1 }}>
                    {enrichedData && enrichedData.length > 0 ? (
                        <>
                            <Typography>Select data chips to include them in the AI report outline</Typography>
                            {enrichedData.map((data: any, index: number) => (
                                <Card key={index} sx={{ width: '100%', marginTop: 0, marginBottom: 2 }}>
                                    <Typography level='h3'>{data.category}</Typography>
                                    <Sheet sx={{ alignItems: 'center', overflowX: 'auto', flexWrap: 'nowrap' }}>
                                        <Chip
                                            size="lg"
                                            variant={selectedData.includes(`${data.category} ${data.data1_time} ${data.data1_type}: ${data.data1_value} ${data.unit}`) ? 'solid' : 'soft'}
                                            color='primary'
                                            sx={{ marginRight: 1, marginBottom: 1 }}
                                            onClick={() => handleChipClick(data)}
                                        >
                                            {data.data1_time} {data.data1_type}: {data.data1_value} {data.unit}
                                        </Chip>
                                        <Chip
                                            size="lg"
                                            variant={selectedData.includes(`${data.category} ${data.data2_time} ${data.data2_type}: ${data.data2_value} ${data.unit}`) ? 'solid' : 'soft'}
                                            color='primary'
                                            sx={{ marginRight: 0, marginBottom: 1 }}
                                            onClick={() => handleChipClick({ ...data, category: data.category, data1_time: data.data2_time, data1_type: data.data2_type, data1_value: data.data2_value })}
                                        >
                                            {data.data2_time} {data.data2_type}: {data.data2_value} {data.unit}
                                        </Chip>
                                    </Sheet>
                                    <Typography sx={{ marginTop: 0 }}>{data.reasoning}</Typography>
                                </Card>
                            ))}
                        </>
                    ) : (
                        <Typography>To see data insights, first start and end a transcription.</Typography>
                    )}
                </Sheet>
            )}

            <Button size='lg' onClick={handleOutlineGenerator} sx={{ marginTop: 2 }}>
                ✨ Generate Outline From Selected Data and Transcript ✨
            </Button>
        </Card>
    );
}
