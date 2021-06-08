import * as React from "react";
import Head from "next/head";
import { AppProps } from "next/app";
import { ThemeProvider } from "@material-ui/core/styles";
import CssBaseline from "@material-ui/core/CssBaseline";
import { CacheProvider } from "@emotion/react";
import createCache from "@emotion/cache";
import theme from "@libs/theme";

import { ApolloClient, InMemoryCache, ApolloProvider } from "@apollo/client";

const materialUiCache = createCache({ key: "css", prepend: true });
materialUiCache.compat = true;

const cache = new InMemoryCache();
const client = new ApolloClient({
  uri: `${process.env.NEXT_PUBLIC_BACKEND_URL}/graphql`,
  cache,
});

export default function MyApp(props: AppProps) {
  const { Component, pageProps } = props;
  return (
    <ApolloProvider client={client}>
      <CacheProvider value={materialUiCache}>
        <Head>
          <title>My page</title>
          <meta name="viewport" content="initial-scale=1, width=device-width" />
        </Head>
        <ThemeProvider theme={theme}>
          {/* CssBaseline kickstart an elegant, consistent, and simple baseline to build upon. */}
          <CssBaseline />
          <Component {...pageProps} />
        </ThemeProvider>
      </CacheProvider>
    </ApolloProvider>
  );
}
