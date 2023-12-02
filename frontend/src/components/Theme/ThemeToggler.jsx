import { FormLabel, Switch, useColorMode } from "@chakra-ui/react";

export const ThemeToggler = ({ showLabel = false, ...rest }) => {
  const { toggleColorMode, colorMode } = useColorMode();
  return (
    <>
      {showLabel && (
        <FormLabel htmlFor="theme-toggler" mb={0}>
          <p>Dark Mode</p>
        </FormLabel>
      )}
      <Switch
        white-space="pre-wrap"
        id="theme-toggler"
        size="sm"
        isChecked={colorMode === "dark"}
        isDisabled={false}
        value={colorMode}
        colorScheme="teal"
        mr={2}
        onChange={toggleColorMode}
        {...rest}
      />
    </>
  );
};
