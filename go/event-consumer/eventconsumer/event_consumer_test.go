package eventconsumer

import (
	"bytes"
	"os"
	"testing"

	"gopkg.in/yaml.v3"
)

func TestLoad(t *testing.T) {
	prefs := Preferences{
		FromEmail:         "foo.com",
		ToEmail:           "bar.com",
		NotificationDelay: "10",
	}

	prefsBytes := new(bytes.Buffer)

	if err := yaml.NewEncoder(prefsBytes).Encode(prefs); err != nil {
		t.Fatal(err)
	}
	if err := os.MkdirAll("testdata", 0755); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile("testdata/preferences_test.yaml", prefsBytes.Bytes(), 0644); err != nil {
		t.Fatal(err)
	}

	notifier := EventConsumer{}
	notifier.Load("testdata/preferences_test.yaml")

	if notifier.Prefs.NotificationDelay != "10" {
		t.Fatalf("Notification delay was not 10")
	}

	if notifier.Prefs.FromEmail != "foo.com" {
		t.Fatalf("From email was not foo.com")
	}

	if notifier.Prefs.ToEmail != "bar.com" {
		t.Fatalf("From email was not bar.com")
	}

}
