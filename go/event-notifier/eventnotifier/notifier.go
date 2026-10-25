package eventnotifier

import (
	"log"
	"os"

	"gopkg.in/yaml.v3"
)

type Notifier struct {
	Prefs Preferences
}

func (n *Notifier) SetPrefs(prefs Preferences) {
	n.Prefs.NotificationDelay = prefs.NotificationDelay
	n.Prefs.Sysadminemail = prefs.Sysadminemail
}

func (n *Notifier) Load(prefsFile string) (bool, error) {
	prefs := Preferences{
		Sysadminemail:     "",
		NotificationDelay: "0",
	}

	f, err := os.ReadFile(prefsFile)
	if err != nil {
		log.Println("No preferences file found")
		return false, err
	} else {
		if err := yaml.Unmarshal(f, &prefs); err != nil {
			log.Println("Unmarshal failed")
			return false, err
		} else {
			log.Println("Successfully unmarshalled preferences")
			n.Prefs = prefs
			return true, nil
		}
	}
}

func (n Notifier) SendNotification(msg string) {
	log.Printf("Sending notification: (%v) to %v", msg, n.Prefs.Sysadminemail)
}
