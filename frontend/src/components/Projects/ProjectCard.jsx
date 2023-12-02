import { Badge, Flex, Text, useColorModeValue } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";

export const ProjectCard = ({ project }) => {
  const navigate = useNavigate();
  return (
    <Flex
      bg={useColorModeValue("gray.300", "gray.600")}
      minHeight="3rem"
      my={3}
      p={3}
      rounded="lg"
      alignItems="center"
      justifyContent="space-between"
      _hover={{
        opacity: 0.9,
        cursor: "pointer",
        transform: "translateY(-3px)",
      }}
      onClick={() => navigate(`/${project.project_id}`, { replace: true })}
    >
      <Text>{project.title}</Text>
      <Badge colorScheme={project.status ? "green" : "purple"}>
        {project.status ? "Complete" : "Pending"}
      </Badge>
    </Flex>
  );
};
