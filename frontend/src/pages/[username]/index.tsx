import Layout from "@components/UserPageLayout";
import { useRouter } from "next/router";
import { useSession } from "next-auth/client";

const UserPage = () => {
  const router = useRouter();
  const session = useSession();
  const { username } = router.query;
  console.log(session);
  return (
    <Layout>
      <p>test in {username}</p>
    </Layout>
  );
};

export default UserPage;
