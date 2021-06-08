import React from "react";

import Layout from "@components/Layout";

const index = () => {
  return (
    <Layout>
      <h1>test</h1>
      <p>{process.env.NEXT_PUBLIC_BACKEND_URL}</p>
      <p>a</p>
    </Layout>
  );
};

export default index;
