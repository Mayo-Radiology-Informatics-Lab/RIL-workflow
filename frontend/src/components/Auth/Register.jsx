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
import axiosInstance from "../../services/axios";
import { ThemeToggler } from "../Theme/ThemeToggler";

export const Register = () => {
  const {
    handleSubmit,
    register,
    formState: { errors, isSubmitting },
  } = useForm();
  const navigate = useNavigate();
  const toast = useToast();

  const onSubmit = async (values) => {
    try {
      await axiosInstance.post("/users/create", values);
      toast({
        title: "Account created successfully.",
        status: "success",
        isClosable: true,
        duration: 1500,
      });
      navigate("/login", { replace: true });
    } catch (err) {
      toast({
        title: `${err.response.data.detail}`,
        status: "error",
        isCloseable: true,
        duration: 1500,
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
        <Heading mb={6} fontSize={20}>Register</Heading>
        <form onSubmit={handleSubmit(onSubmit)} justifyContent='center'>

          <FormControl isInvalid={errors.email}>
            <Input 
              type="email"
              placeholder="Email" 
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

          <FormControl isInvalid={errors.username}>
            <Input 
              type="text"
              placeholder="Username" 
              {...register("username", {
                required: "This is required",
                minLength: {
                  value: 5,
                  message: "Minimum length should be 5",
                },
                maxLength: {
                  value: 20,
                  message: "Maximum length should be 20",
                },
              })}
              size="lg"
              mt={3}
              backgroundColor={useColorModeValue("#ffffff", "#1c1c1c")}
            />
            <FormErrorMessage>
              {errors.username && errors.username.message}
            </FormErrorMessage>
          </FormControl>

          <FormControl isInvalid={errors.password}>
            <Input 
              type="password"
              placeholder="password" 
              {...register("password", {
                required: "This is required",
                minLength: {
                  value: 5,
                  message: "Minimum length should be 5",
                },
                maxLength: {
                  value: 20,
                  message: "Maximum length should be 20",
                },
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
            width={'100%'} colorScheme="teal" size="lg" mt={3} type="submit">
            Register
          </Button>
        </form>
        <Button mt={2}>
          <ThemeToggler showLabel={true}/>
        </Button>

        <Button onClick={() => navigate("/login", { replace: true })}
          width={'100%'} colorScheme="gray" size="lg" mt={3}>
          Login
        </Button>
        
      </Flex>
    </Flex>
  );
};
