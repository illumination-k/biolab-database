import NextAuth from 'next-auth'
import Providers from 'next-auth/providers'

import { gql } from "@apollo/client"
import client from "@libs/initApollo"

const AUTH_QUERY = gql`
    mutation AuthUser($username: String!, $password: String!) {
        auth(username: $username, password: $password) {
            token,
            username
        }
    }
`;

const providers = [
    Providers.Credentials({
        name: 'Credentials',
        authorize: async (credential) => {
            try {// graphql
            const { data } = await client.mutate({
                    mutation: AUTH_QUERY,
                    variables: {username: credential.email, password: credential.password}
                },
            )

            console.log(data)

            if (data) {
                return { status: "success", token: data.auth.token }
            }

            } catch (e) {
                const message = e.response.data.message
                throw new Error(message)
            }

        }     
    })
]

const callbacks = {
    async jwt(token, user) {

        if (user) {
            token.accessToken = user.token
        }

        return token
    },

    async session(session, token) {
        console.log(token)
        session.accessToken = token.accessToken
        return session
    }


}

const options = {
    providers,
    callbacks,
    pages: {
        error: '/login' // Changing the error redirect page to our custom login page
    }
}

export default (req, res) => NextAuth(req, res, options)