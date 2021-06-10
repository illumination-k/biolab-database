import Layout from "@components/Layout";
import UserPageAppBar from "@components/UserPageAppBar";

const UserPageLayout = ({ children }) => {
  return (
    <Layout>
      <UserPageAppBar />
      {children}
    </Layout>
  );
};

export default UserPageLayout;
