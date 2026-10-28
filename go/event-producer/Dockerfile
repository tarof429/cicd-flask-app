# syntax=docker/dockerfile:1

FROM golang:alpine3.24 AS builder

# Set destination for COPY
WORKDIR /app

# Download Go modules
COPY go.mod go.sum ./
RUN go mod download

COPY . .

# Build
RUN CGO_ENABLED=0 GOOS=linux go build -o event-producer

FROM alpine:3.24

WORKDIR /app

COPY --from=builder /app/event-producer .

# Run
CMD ["./event-producer"]
#CMD ["tail", "-f", "/dev/null"]
