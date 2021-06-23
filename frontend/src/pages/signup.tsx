import React from "react";

import { useForm, Controller, SubmitHandler } from "react-hook-form";
import { TextField, Button, Grid } from "@material-ui/core";

interface SignUpUser {
  username: string;
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  birthDay: string;
}

interface Meta {
  name: string;
  label: string;
  type: "text" | "email" | "password" | "date";
}

const SignUpPage = () => {
  const { control, handleSubmit } = useForm();

  // dataをmutationする
  const onSubmit: SubmitHandler<SignUpUser> = (data) => console.log(data);

  const metas: Array<Meta> = [
    {
      name: "username",
      label: "User Name",
      type: "text",
    },
    {
      name: "email",
      label: "E-mail",
      type: "email",
    },
    {
      name: "password",
      label: "Password",
      type: "password",
    },
    {
      name: "repassword",
      label: "Re-type Password",
      type: "password"
    },
    {
      name: "firstName",
      label: "First Name",
      type: "text",
    },
    {
      name: "lastName",
      label: "Last Name",
      type: "text",
    },
    {
      name: "birthDay",
      label: "Birthday",
      type: "date",
    },
  ];

  const inputFields = metas.map((v, i) => (
    <Grid key={i}>
      <Controller
        name={v.name}
        key={i}
        control={control}
        render={({ field }) => (
          <TextField
            label={v.label}
            required
            type={v.type}
            InputLabelProps={{
              shrink: true,
            }}
            {...field}
          />
        )}
      />
    </Grid>
  ));

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {inputFields}
      <Button
        type="submit"
        color="primary"
        variant="contained"
        style={{ marginTop: "0.5rem" }}
      >
        Sign Up
      </Button>
    </form>
  );
};

export default SignUpPage;
