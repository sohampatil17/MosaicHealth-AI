import { Button, Card, Typography, Sheet, Chip, CircularProgress, Box } from '@mui/joy';
import { useEffect, useState } from 'react';

interface DataInsightsProps {
    importantData: any;
    loadingDataSuggestions: boolean;
    setOutline: React.Dispatch<React.SetStateAction<string>>
}

export default function DataInsights({ importantData, loadingDataSuggestions, setOutline }: DataInsightsProps) {
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
            const enrichedData = importantData.map((dataPoint: { category: string | number; data1_time: string | number; data1_type: string | number; data2_time: string | number; data2_type: string | number; }) => {
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

    // Function to handle generating the initial report
    const handleOutlineGenerator = () => {

        setOutline("AI generated this magical outline")
    }

    return (
        <Card color='primary' sx={{ margin: 2, marginRight: 0, justifyItems: 'top', alignItems: 'center' }}>
            <Typography level='h3'>Data Insights</Typography>

            {loadingDataSuggestions ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '56vh' }}>
                    <CircularProgress />
                </Box>
            ) : (
                <Sheet sx={{ width: '100%', minHeight: '56vh', overflowY: 'auto' }}>
                    {enrichedData && enrichedData.length > 0 ? (
                        <>
                            <Typography>Select data chips to include them in the AI report outline</Typography>
                            {enrichedData.map((data: any, index: number) => (
                                <Card key={index} sx={{ width: '100%', marginTop: 0, marginBottom: 2 }}>
                                    <Typography level='h3'>{data.category}</Typography>
                                    <Sheet sx={{ alignItems: 'center', overflowX: 'auto', flexWrap: 'nowrap' }}>
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
                                            onClick={() => handleChipClick({ ...data, data1_time: data.data2_time, data1_type: data.data2_type, data1_value: data.data2_value })}
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
