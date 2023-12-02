import { Flex, Spinner } from "@chakra-ui/react";
import {
  BrowserRouter as Router,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";
import { Authenticated } from "./components/Auth/Authenticated";
import { Login } from "./components/Auth/Login";
import { PublicRoute } from "./components/Auth/PublicRoute";
import { Register } from "./components/Auth/Register";
import { NavBar } from "./components/Navbar/NavBar";
import { ContentList } from "./components/Projects/ContentList";
import { ProjectList } from "./components/Projects/ProjectList";
import { AuthUser, AuthProvider } from "./context/JWTAuthContext";

function App() {
  return (
    <>
      <AuthProvider>
        <Router>
          <AuthUser>
            {(auth) =>
              !auth.isInitialized ? (
                <Flex
                  height="100vh"
                  alignItems="center"
                  justifyContent="center"
                >
                  <Spinner
                    thickness="4px"
                    speed="0.65s"
                    emptyColor="green.200"
                    color="green.500"
                    size="xl"
                  />
                </Flex>
              ) : (
                <Routes>
                  <Route
                    path="/login"
                    element={
                      <PublicRoute>
                        <Login />
                      </PublicRoute>
                    }
                  />
                  <Route
                    path="/register"
                    element={
                      <PublicRoute>
                        <Register />
                      </PublicRoute>
                    }
                  />
                  <Route path="/" element={<NavBar />}>
                    <Route
                      path="/"
                      element={
                        <Authenticated>
                          <ProjectList />
                        </Authenticated>
                      }
                    />
                    <Route
                      path="/:project_id"
                      element={
                        <Authenticated>
                          <ContentList />
                        </Authenticated>
                      }
                    />
                  </Route>
                  <Route path="*" element={<Navigate to="/" />} />
                </Routes>
              )
            }
          </AuthUser>
        </Router>
      </AuthProvider>
    </>
  );
}

export default App;