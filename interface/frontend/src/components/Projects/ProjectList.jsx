import { Box, Center, Container, Spinner } from "@chakra-ui/react";
import { useEffect, useRef, useState } from "react";
import axiosInstance from "../../services/axios";
import { AddUpdateProjectModel } from "./AddUpdateProjectModel";
import { ProjectCard } from "./ProjectCard";

export const ProjectList = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const isMounted = useRef(false);
  

  useEffect(() => {
    if (isMounted.current) return;
    fetchProjects();
    isMounted.current = true;
  }, []);

  const fetchProjects = () => {
    setLoading(true);
    axiosInstance
      .get("/projects/")
      .then((res) => {
        setProjects(res.data);
      })
      .catch((error) => {
        console.error(error);
      })
      .finally(() => {
        setLoading(false);
      });
  };



  return (
    <Container mt={9}>
      <AddUpdateProjectModel onSuccess={fetchProjects} />
      {loading ? (
        <Center mt={6}>
          <Spinner
            thickness="4px"
            speed="0.65s"
            emptyColor="green.200"
            color="green.500"
            size="xl"
          />
        </Center>
      ) : (
        <Box mt={6}>
          {projects?.map((project) => (
            <ProjectCard project={project} key={project.id} />
          ))}
        </Box>
      )}
    </Container>
  )
};
