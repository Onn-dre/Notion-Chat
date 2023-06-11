import { ConnectWallet, useAddress, Web3Button } from "@thirdweb-dev/react";
import Link from "next/link";
import styles from "../styles/Home.module.css";

export default function Login() {
  const address = useAddress(); // Get the user's address

  return (
    <div className={styles.container}>
      <h1 className={styles.h1}>Welcome to Notion Chat!</h1>
      <p className={styles.explain}>
      Quickly find infomation, produce summaries, or ask questions in any database within your Notion workspace
      </p>

      <p className={styles.explain}>
        To access the{" "}
        <Link className={styles.purple} href="/">
          Home Page
        </Link>{" "}
        you must hold an early access NFT from our collection 
      </p>

      <hr className={styles.divider} />

      <>
        {address ? (
          <p>
            Welcome, {address?.slice(0, 6)}...{address?.slice(-4)}
          </p>
        ) : (
          <p>Please connect your wallet to continue.</p>
        )}

        <ConnectWallet accentColor="#F213A4" />
      </>
    </div>
  );
}
