# syntax=docker/dockerfile:1

FROM golang:alpine3.24 AS builder

# Set destination for COPY
WORKDIR /app

# Download Go modules
COPY go.mod ./
RUN go mod download

COPY . .

# Build
RUN CGO_ENABLED=0 GOOS=linux go build -o stresstool

FROM alpine:3.24

WORKDIR /app

COPY --from=builder /app/stresstool .


# Run
CMD ["./stresstool"]
