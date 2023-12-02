import { useEffect, useRef, useState } from "react";
import { useParams } from "react-router-dom";
import axiosInstance from "../../services/axios";
import {
  Button,
  Center,
  Container,
  Spinner,
  Text,
  VStack,
  Checkbox,
  Table,
  TableContainer,
  Tbody,
  Th,
  Thead,
  Tr,
  Td,
  useColorModeValue,
  Box,
  extendTheme,
  ChakraProvider,
  Divider,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
  Select,
  Stack,
  Flex,
} from "@chakra-ui/react";

export const ContentList = () => {
  const [contents, setContents] = useState([]);
  const [headers, setHeaders] = useState([]);
  const [loading, setLoading] = useState(true);
  const isMounted = useRef(false);
  const { project_id } = useParams();
  const background = useColorModeValue("#595959", "#1c1c1c");
  const [selectedRow, setSelectedRow] = useState(null);
  const [selectedHeaders, setSelectedHeaders] = useState([]);
  const ALL_STATUS = "all";
  const INCLUDED_STATUS = true;
  const EXCLUDED_STATUS = false;
  const REMAINING_STATUS = null;
  const [uploadError, setUploadError] = useState(null);
  const [uploadSuccess, setUploadSuccess] = useState(null);
  const [filteredStatus, setFilteredStatus] = useState(ALL_STATUS);
  const [autoProceed, setAutoProceed] = useState(true);
  const [isNextButtonEnabled, setIsNextButtonEnabled] = useState(true);

  const [selectedRowIndex, setSelectedRowIndex] = useState(-1); // Add this state variable


useEffect(() => {
  const handleKeyDown = (event) => {
    if (event.key === "ArrowDown") {
      setSelectedRowIndex(prevIndex => Math.min(prevIndex + 1, filteredContents.length - 1));
    } else if (event.key === "ArrowUp") {
      setSelectedRowIndex(prevIndex => Math.max(prevIndex - 1, 0));
    }
  };
window.addEventListener("keydown", handleKeyDown);

// Cleanup
return () => {
  window.removeEventListener("keydown", handleKeyDown);
};
}, []);

  
//load button 
const [uploadStatus, setUploadStatus] = useState('idle'); // new state variable

  // text
  const greenTextColor = useColorModeValue("green.500", "green.200");
const redTextColor = useColorModeValue("red.500", "red.200");
const orangeTextColor = useColorModeValue("orange.500", "orange.200");

const { isOpen: isConfigModalOpen, onOpen: openConfigModal, onClose: closeConfigModal } = useDisclosure();
const { isOpen: isViewWorkflowModalOpen, onOpen: openViewWorkflowModal, onClose: closeViewWorkflowModal } = useDisclosure();
const { isOpen: isNoDataModalOpen, onOpen: openNoDataModal, onClose: closeNoDataModal } = useDisclosure();

useEffect(() => {
  if (filteredContents.length === 0) {
    openNoDataModal();
  }
}, []);


  const [checkedItems, setCheckedItems] = useState([false, false])

  const allChecked = checkedItems.every(Boolean)
  const isIndeterminate = checkedItems.some(Boolean) && !allChecked

  useEffect(() => {
    if (isMounted.current) return;
    fetchContents();
    isMounted.current = true;
  }, [project_id]);

  const fileUpload = (e) => {
    setUploadError(null); // Clear any previous error messages
    setUploadSuccess(null);
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append("file", file);
    axiosInstance
        .post(`/contents/${project_id}/upload`, formData)
        .then((res) => {
            if(res.data.code == 500){
              setUploadError(res.data.message)
            }
            if(res.data.code == 200){
              setUploadSuccess(res.data.message)
              setUploadStatus("uploading")
            }
            console.log(res);
            // fetchContents(); Uncomment this if you have a fetchContents function
        })
        .catch((error) => {
            console.error(error);
            // Set the error message if the upload fails
            setUploadError(error.response?.data?.message || "An error occurred during file upload.");
        })
        .finally(() => {
            setLoading(false);
        });
};


const [isRadiologyReportChecked, setIsRadiologyReportChecked] = useState(false);
const [isImpressionChecked, setIsImpressionChecked] = useState(false);


  const fetchContents = () => {
    setLoading(true);
    axiosInstance
      .get(`/contents/${project_id}`)
      .then((res) => {
        setContents(res.data);
        if (res.data.length > 0) {
          console.log(res.data[0].other_content);
          const keys = Object.keys(res.data[0].other_content[0]);
          setHeaders(keys);
        }
      })
      .catch((error) => console.error(error))
      .finally(() => {
        setLoading(false);
      });
  };

  const theme = extendTheme({
    components: {
      Table: {
        baseStyle: {
          td: {
            _hover: {bg: "green.100",}
          }
        }
      }
    }
  }
  );

  const handleRowSelection = (rowId) => {
    if (selectedRow === rowId) {
      setSelectedRow(null);
    } else {
      setSelectedRow(rowId);
    }
  };

  const updateContentStatus =(rowId, status) => {
    setLoading(true);
    axiosInstance
      .put(`/contents/${project_id}/${rowId}`, {
        status: status,
      })
      .then((res) => {
        console.log(res);
        fetchContents();
      })
      .catch((error) => console.error(error))
      .finally(() => {
        setLoading(false);
      });
  };

  const handleHeaderSelection = (header) => {
    if (selectedHeaders.includes(header)) {
      setSelectedHeaders(selectedHeaders.filter((h) => h !== header));
    } else {
      setSelectedHeaders([...selectedHeaders, header]);
    }
  };

  const getCellValue = (row, header) => {
    const content = contents.find((c) => c.content_id === row);
    if (content && content.other_content) {
      const item = content.other_content.find((item) => item[header]);
      if (item) {
        return item[header];
      }
    }
    return "";
  };
  
  // Filter the contents based on the selected status
  const filteredContents = contents.filter((content) => {
    if (filteredStatus === ALL_STATUS) {
      return true; // Show all contents
    } else if (filteredStatus === INCLUDED_STATUS) {
      return content.status === true; // Show included contents
    } else if (filteredStatus === EXCLUDED_STATUS) {
      return content.status === false; // Show excluded contents
    } else if (filteredStatus === REMAINING_STATUS) {
      return content.status === null; // Show remaining contents (null status)
    } else {
      return false; // Invalid status, don't show any contents
    }
  });

  // Handler for the filter buttons
  const handleFilter = (status) => {
    setFilteredStatus(status);
  };

  if (loading) {
    return (
      <Container mt={6}>
        <Center mt={6}>
          <Spinner
            thickness="4px"
            speed="0.65s"
            emptyColor="green.200"
            color="green.500"
            size="xl"
          />
        </Center>
      </Container>
    );
  }

 
  const includeAllContents = () => {
    filteredContents.forEach(content => {
        updateContentStatus(content.content_id, true);
    });
};

const includeAllRemainingContents = () => {
  const remainingContents = contents.filter(content => content.status === null);
  remainingContents.forEach(content => {
      updateContentStatus(content.content_id, true);
  });
};

const selectedContent = contents.find(content => content.content_id === selectedRow);
let statusDisplay = null;

if (selectedContent) {
    const { status } = selectedContent;
    let selectedRowStatus = "";
    let textColor = "";
    if (status === true) {
        selectedRowStatus = "Included";
        textColor = greenTextColor;
    } else if (status === false) {
        selectedRowStatus = "Excluded";
        textColor = redTextColor;
    } else {
        selectedRowStatus = "Remaining";
        textColor = orangeTextColor;
    }

    statusDisplay = <Text fontWeight="bold" mt={2} color={textColor}>Status: {selectedRowStatus}</Text>;
}

  return (
    <>

   

<Modal isOpen={isConfigModalOpen} onClose={closeConfigModal}>
  <ModalOverlay />
  <ModalContent>
    <ModalHeader>Settings</ModalHeader>
    <ModalCloseButton />
    <ModalBody>
    <div>
      <div style={{ marginBottom: '10px' }}>
      <Text marginBottom="2px" fontWeight="bold">Upload Data</Text>
      <Text marginBottom="2px">The data uploaded should be in a .CSV, .XLSX, or .XLS format and have the fields <code>accession_id</code>, <code>clinic_id</code>, <code>report_id</code>, <code>report_date</code>, <code>modalities</code>, and <code>other_content</code>.</Text>
      <Text marginBottom="1px" fontWeight="bold" color="red">{uploadError}</Text>
      <Text marginBottom="5px" fontWeight="bold" color="green">{uploadSuccess}</Text>
      <div style={{ marginBottom: '10px' }}>
      <Button
  variant='outline'
  disabled={uploadStatus === 'uploading'} // Disable the button while uploading
  onClick={(e) => {
    // Trigger file input when button is clicked
    e.target.nextSibling.click();
  }}
>
  {uploadStatus === 'uploading' ? "Success - refresh to upload another file" : uploadStatus === 'error' ? "Error" : "Upload File"}
</Button>
<Text marginBottom="2px" fontWeight="bold" marginTop="2px">Enter your final storing pathway</Text>
<input type="text" id="path" name="path" placeholder="e.g. /research/ ..." style={{ width: '70%'}} borderWidth="1px solid gray"
  ></input>
<input
  type="file"
  onChange={fileUpload}
  style={{ display: 'none' }}
  placeholder="Add list"
  disabled={uploadStatus === 'uploading'} // Disable the input while uploading
/>



      </div>
        </div>
        <Box marginTop="10px" marginBottom="10px">
            <Text marginBottom="8px" fontWeight="bold">Select Workflow</Text>
            <Select size='md' defaultValue="workflow1">
                <option value="workflow1">Workflow 1 (Default)</option>
                <option value="workflow2">Workflow 2</option>
                <option value="workflow3">Workflow 3</option>
                <option value="workflow4">Workflow 4</option>
            </Select>
            
        </Box>
        </div>
        <div>
        
      <Box marginTop="10px" marginBottom="10px">
        <Text marginBottom="8px" fontWeight="bold">Table View</Text>
        
      <Stack pl={6} mt={1} spacing={1}>
      {headers.map((header) => (
                
                <Checkbox
                  isChecked={selectedHeaders.includes(header)}
                  onChange={() => handleHeaderSelection(header)}
                >
                  {header}
                </Checkbox>
              
              ))}
</Stack>

      </Box>
      <Box marginTop="10px" marginBottom="10px">
        <Text marginBottom="8px" fontWeight="bold">Other Settings</Text>
        
      <Stack pl={6} mt={1} spacing={1}>
      <Checkbox>Hide empty columns</Checkbox>
      <Checkbox onChange={(e) => setAutoProceed(e.target.checked)} defaultChecked>
  Automatically proceed next after selection
</Checkbox>
<Checkbox
  defaultChecked
  onChange={(e) => setIsNextButtonEnabled(e.target.checked)}
>
  Enable Next Button
</Checkbox>


</Stack>

      </Box>
        </div>
    </ModalBody>

    <ModalFooter>
    <Button onClick={closeConfigModal}>Close</Button>
    </ModalFooter>
  </ModalContent>
</Modal>

<Modal onClose={closeViewWorkflowModal} isOpen={isViewWorkflowModalOpen} isCentered>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Camunda Workflow</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <div>
            Realtime view of the Camunda workflow engine processing your requests.
              </div>
          </ModalBody>
          <ModalFooter>
            <Button onClick={closeViewWorkflowModal}>Close</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
      {
  filteredContents.length === 0 && isNoDataModalOpen && (
    <Modal isOpen={isNoDataModalOpen} onClose={closeNoDataModal}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Upload Data</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <Text>Hi! Looks like you need to populate your table with some data. The data uploaded should be in a .CSV, .XLSX, or .XLS format and have the fields <code>accession_id</code>, <code>clinic_id</code>, <code>report_id</code>, <code>report_date</code>, <code>modalities</code>, and <code>other_content</code>.</Text>
          <Text marginBottom="0px" fontWeight="bold" color="red">{uploadError}</Text>
          <Text marginBottom="0px" fontWeight="bold" color="green">{uploadSuccess}</Text>
        </ModalBody>
        <ModalFooter>
        <Button
  variant='outline'
  disabled={uploadStatus === 'uploading'} // Disable the button while uploading
  onClick={(e) => {
    // Trigger file input when button is clicked
    e.target.nextSibling.click();
  }}
>
  {uploadStatus === 'uploading' ? "Success - refresh to upload another file" : uploadStatus === 'error' ? "Error" : "Upload File"}
</Button>
<input
  type="file"
  onChange={fileUpload}
  style={{ display: 'none' }}
  placeholder="Add list"
  disabled={uploadStatus === 'uploading'} // Disable the input while uploading
/>

        </ModalFooter>
      </ModalContent>
    </Modal>
  )
}

       
<Flex alignItems="center" marginTop="10px" marginBottom="10px">
    <Flex alignItems="center" marginRight="auto">
        <Button size="sm" onClick={openConfigModal} marginLeft="8px" marginRight="4px">
            Settings
        </Button>

        <Button size="sm" onClick={openViewWorkflowModal} marginLeft="4px">
            View Workflow
        </Button>
    </Flex>

    <Box>
        <Button
            size="sm"
            mr="8px"
            colorScheme={filteredStatus === ALL_STATUS ? "blue" : "gray"}
            onClick={() => handleFilter(ALL_STATUS)}
        >
            All
        </Button>
        <Button
            size="sm"
            mr="8px"
            colorScheme={filteredStatus === INCLUDED_STATUS ? "green" : "gray"}
            onClick={() => handleFilter(INCLUDED_STATUS)}
        >
            Included
        </Button>
        <Button
            size="sm"
            mr="8px"
            colorScheme={filteredStatus === EXCLUDED_STATUS ? "red" : "gray"}
            onClick={() => handleFilter(EXCLUDED_STATUS)}
        >
            Excluded
        </Button>
        <Button
            size="sm"
            mr="8px"
            colorScheme={filteredStatus === REMAINING_STATUS ? "orange" : "gray"}
            onClick={() => handleFilter(REMAINING_STATUS)}
        >
            Remaining
        </Button>
    </Box>
</Flex>


      <ChakraProvider theme={theme}>
        <TableContainer
          maxH={ selectedHeaders.length > 0 ? "40vh" : "87.5vh" }
          maxW="100vw"
          overflowX="auto"
          overflowY="auto"
          width={'100%'} overflow={'auto'}
        >
          <Table
            variant="simple"
            border="1px solid gray"
            tableLayout="fixed"
            width="100%"
            size="sm"
          >
            <Thead
              color="white"
              backgroundColor={background}
              position="sticky"
              top={0}
              zIndex={1}
            >
              <Tr>
                <Th color="white">Accession ID</Th>
                <Th color="white">Clinic ID</Th>
                <Th color="white">Report ID</Th>
                <Th color="white">Report Date</Th>
                <Th color="white">Modality</Th>
                <Th color="white">Radiology Report</Th>
                <Th color="white">Impression</Th>
                
                <Th color="white">Status</Th>
              </Tr>
            </Thead>
            <Tbody>
            {filteredContents.map((content, index) => (
                <Tr
                key={content.content_id}
                onClick={() => {
                  handleRowSelection(content.content_id);
                  setSelectedRowIndex(index);
                }}
                cursor="pointer"
                backgroundColor={selectedRow === content.content_id ? "green.200" : "transparent"}
                color={selectedRow === content.content_id ? "black" : "inherit"}
                _hover={{ backgroundColor: "green.100", color: "black" }}
            >
            
                  <Td>{content.accession_id}</Td>
                  <Td>{content.clinic_id}</Td>
                  <Td>{content.report_id}</Td>
                  <Td>{content.report_date}</Td>
                  <Td>{content.modality}</Td>
                  {headers.map((header) => (
                    <Td
                      key={`${content.content_id}-${header}`}
                      style={{
                        maxWidth: "100px",
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        whiteSpace: "nowrap",
                      }}
                    >
                      {content.other_content
                        ? content.other_content
                            .map((item) => item[header])
                            .join(", ")
                        : ""}
                    </Td>
                  ))}
                  <Td>
                    {content.status === true ? "Included" : ""}
                    {content.status === false ? "Excluded" : ""}
                    {content.status === null ? "Remaining" : ""}
                  </Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        </TableContainer>
        {
    selectedRow && selectedHeaders.length > 0 && (
      <Box 
      borderWidth="1px" 
      borderRadius="md" 
      p={4}
      style={{
          overflowY: "auto",
          maxHeight: "50vh" // You can adjust this value
      }}
  >
      <Box mt={2}>
      <Button
          size="sm"
          colorScheme="cyan"
          marginRight="10px"
          isDisabled={contents.find(content => content.content_id === selectedRow)?.status === true}
          onClick={() => {
              updateContentStatus(selectedRow, true);
              if (autoProceed && selectedRowIndex < filteredContents.length - 1) {
                  const newIndex = selectedRowIndex + 1;
                  setSelectedRowIndex(newIndex);
                  handleRowSelection(filteredContents[newIndex].content_id);
              }
          }}
      >
          Include
      </Button>

      <Button
          size="sm"
          colorScheme="red"
          marginRight="10px"
          isDisabled={contents.find(content => content.content_id === selectedRow)?.status === false}
          onClick={() => {
              updateContentStatus(selectedRow, false);
              if (autoProceed && selectedRowIndex < filteredContents.length - 1) {
                  const newIndex = selectedRowIndex + 1;
                  setSelectedRowIndex(newIndex);
                  handleRowSelection(filteredContents[newIndex].content_id);
              }
          }}
      >
          Exclude
      </Button>

  
          <Button
              size="sm"
              colorScheme="orange"
              marginRight="10px"
              isDisabled={!contents.some(content => content.status === null)}
              onClick={includeAllRemainingContents}
          >
              Include All Remaining
          </Button>
          {isNextButtonEnabled && (
  <Button
    size="sm"
    colorScheme="blue"
    marginRight="10px"
    isDisabled={selectedRowIndex >= filteredContents.length - 1}
    onClick={() => {
      const newIndex = selectedRowIndex + 1;
      setSelectedRowIndex(newIndex);
      handleRowSelection(filteredContents[newIndex].content_id);
    }}
  >
    Next
  </Button>
)}


  
          {statusDisplay}
  
          {selectedHeaders.map((header) => (
              <Box key={header} mt={2}>
                  <Text fontWeight="bold">{header}:</Text>
                  <Text>{getCellValue(selectedRow, header)}</Text>
              </Box>
          ))}
      </Box>
  </Box>
  
    )
}

      </ChakraProvider>
    </>
  );
};