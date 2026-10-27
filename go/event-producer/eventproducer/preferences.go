package eventproducer

type Preferences struct {
	FromEmail         string `yaml:"from"`
	ToEmail           string `yaml:"to"`
	NotificationDelay string `yaml:"notificationDelay"`
}
