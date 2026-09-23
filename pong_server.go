package main

import (
	"bufio"
	"errors"
	"fmt"
	"io"
	"net"
	"os"
	"strings"
	//"time"
)

const addr = "0.0.0.0:5000"

func handle(conn net.Conn) {
	defer conn.Close()
	fmt.Printf("Robot connected from %s\n", conn.RemoteAddr())

	r := bufio.NewReader(conn)
	for {
		line, err := r.ReadString('\n')
		if err != nil {
			if errors.Is(err, io.EOF) {
				fmt.Println("Robot disconnected.")
			} else {
				fmt.Printf("Read error: %v\n", err)
			}
			return
		}

		msg := strings.TrimSpace(line)
		fmt.Printf("Received: %q\n", msg)

		if msg == "PING" {
			// time.Sleep(2 * time.Second)
			if _, err := io.WriteString(conn, "PONG\n"); err != nil {
				fmt.Printf("Write error: %v\n", err)
				return
			}
			fmt.Println("Sent: PONG")
		} else {
			if _, err := io.WriteString(conn, "ERR unknown\n"); err != nil {
				fmt.Printf("Write error: %v\n", err)
				return
			}
		}
	}
}

func main() {
	ln, err := net.Listen("tcp", addr)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Listen failed: %v\n", err)
		os.Exit(1)
	}
	defer ln.Close()
	fmt.Printf("Listening on %s...\n", addr)

	for { // keep serving new connections
		conn, err := ln.Accept()
		if err != nil {
			fmt.Printf("Accept error: %v\n", err)
			continue
		}
		handle(conn) // one robot at a time, like the Python version
	}
}
