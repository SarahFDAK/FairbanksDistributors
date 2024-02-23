
export const routes = [
    {
      "storeName": "Test",
      "rsr": [""]
    },
    {
        "storeName": "West Freds",
        "rsr": ["Nick T.", "Bill", "Angus", "Aaron"]
    },
    {
        "storeName": "S2754",
        "rsr": ["Nick T.", "Bill", "Angus"]
    },
    {
        "storeName": "S1821",
        "rsr": ["Nick T.", "Bill", "Angus"]
    },
    {
        "storeName": "East Freds",
        "rsr": ["Don", "Carrie", "Nick F."]
    },
    {
        "storeName": "S3410",
        "rsr": ["Don", "Carrie", "Nick F."]
    },
    {
        "storeName": "Walmart",
        "rsr": ["Terry C.", "Ryan", "Shawn", "Duane", "Aaron"]
    },
    {
        "storeName": "Costco",
        "rsr": "Shawn"
    },
    {
        "storeName": "Wainwright Shoppette",
        "rsr": "Terry C."
    },
    {
        "storeName": "Wainwright Commissary",
        "rsr": ["Terry C.", "Ryan"]
    },
    {
      "storeName": "Eielson Commissary",
      "rsr": [""]
    },
    {
      "storeName": "Eielson Shoppette",
      "rsr": [""]
    },
    {
      "storeName": "SD Bulk Plant",
      "rsr": [""]
    },
    {
      "storeName": "Campus Cache",
      "rsr": [""]
    },
    {
      "storeName": "Greely Commissary",
      "rsr": [""]
    },
    {
      "storeName": "Walgreens",
      "rsr": [""]
    },
    {
      "storeName": "Gold Star Liquor",
      "rsr": [""]
    },
    {
      "storeName": "IGA",
      "rsr": [""]
    },
];

export const routeServiceReps = Array.from( new Set(routes
  .map(item => item.rsr)));

export const storeNames = Array.from( new Set(routes
  .map(item => item.storeName)));
