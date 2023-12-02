import {
  Button,
  Flex,
  FormControl,
  FormErrorMessage,
  Heading,
  Input,
  useColorModeValue,
  useToast,
} from "@chakra-ui/react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import { ThemeToggler } from "../Theme/ThemeToggler";

export const Login = () => {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm();

  const navigate = useNavigate();
  const { login } = useAuth();

  const toast = useToast();
  
  const onSubmit = async (values) => {
    try {
      await login(values.email, values.password);
    } catch (error) {
      toast({
        title: "Invalid credentials",
        description: error.message,
        status: "error",
        duration: 1500,
        isClosable: true,
      });
    }
  };


  return (
    <Flex height="100vh" alignItems="center" justifyContent="center" backgroundColor={useColorModeValue("#ffb800", "#595959")}>
      
      <Flex
        direction="column"
        alignItems="center"
        background={useColorModeValue("#ffffff", "#1c1c1c")}
        p={12}
        rounded={6}
      >
        <Heading mb={6} fontSize={40}>RIL workflow</Heading>
        <Heading mb={6} fontSize={20}>Login</Heading>
        <form onSubmit={handleSubmit(onSubmit)} justifyContent='center'>
          <FormControl isInvalid={errors.email}>
            <Input 
              type="text"
              placeholder="Email or Username" 
              {...register("email", {
                required: "This is required" 
              })}
              size="lg"
              mt={3}
              backgroundColor={useColorModeValue("#ffffff", "#1c1c1c")}
            />
            <FormErrorMessage>
              {errors.email && errors.email.message}
            </FormErrorMessage>

          </FormControl>
          <FormControl isInvalid={errors.password}>
            <Input 
              type="password"
              placeholder="password" 
              {...register("password", {
                required: "This is required" 
              })}
              size="lg"
              mt={3}
              backgroundColor={useColorModeValue("#ffffff", "#1c1c1c")}
            />
            <FormErrorMessage>
              {errors.password && errors.password.message}
            </FormErrorMessage>
          </FormControl>
          <Button
            isLoading={isSubmitting}
            loadingText="Logging in..."
            width={'100%'} colorScheme="teal" size="lg" mt={3} type="submit" >
            Login
          </Button>
        </form>
        <Button mt={2}>
          <ThemeToggler showLabel={true}/>
        </Button>

        <Button onClick={() => navigate("/register", { replace: true })}
          width={'100%'} colorScheme="gray" size="lg" mt={3}>
          Register
        </Button>
        
      </Flex>
    </Flex>
  );
};
