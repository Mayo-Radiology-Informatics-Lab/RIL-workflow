import {
  Box,
  Button,
  Flex,
  Stack,
  Text,
  useColorModeValue,
} from "@chakra-ui/react";
import { useNavigate, Outlet } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import { ThemeToggler } from "../Theme/ThemeToggler";

export const NavBar = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  return (
    <Box minHeight="100vh">
      <Flex
        as="nav"
        align="center"
        justify="space-between"
        wrap="wrap"
        padding="0.25rem"
        bg={useColorModeValue("#ffb800", "#1c1c1c")}
        color={useColorModeValue("#1c1c1c", "#ffffff")}
      >
        <Text as="h2" fontSize={15} fontWeight="bold" marginLeft="8px">
          RIL workflow
        </Text>
        <Stack direction="row" align="center" spacing={4}>
          <ThemeToggler size="lg" />
          <Button colorScheme="gray" onClick={() => navigate('/')}>
            Home
          </Button>
          <Button onClick={logout} colorScheme="red">
            Logout
          </Button>
        </Stack>
      </Flex>
      <Outlet />
    </Box>
  );
};
