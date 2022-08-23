class Data:
    def __init__(self, full_name="", first_name="", mailing_address="", mailing_zip="", mailing_state="",
                 mailing_city="", property_address="", owner_type=""):
        self.full_name = full_name
        self.first_name = first_name
        self.mailing_address = mailing_address
        self.mailing_city = mailing_city
        self.mailing_state = mailing_state
        self.mailing_zip = mailing_zip
        self.property_address = property_address
        self.owner_type = owner_type
        self.row = ""


States = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA",
          "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
          "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "DC", "TEXAS"]
