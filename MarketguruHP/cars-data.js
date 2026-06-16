// Market Guru HP - Database Connector with MySQL API Connection & LocalStorage Fallback

const DEFAULT_USED_CARS = [
  { id: 1, name: 'Maruti Swift VXi', year: 2021, price: '5.20', priceN: 520000, km: '32,000', fuel: 'Petrol', trans: 'Manual', owner: '1st', color: '#e8eef5', emoji: '🚗', verified: true, emi: '9,800', features: ['Power Windows', 'Airbags', 'ABS', 'Bluetooth'], city: 'Vadodara', desc: 'Well maintained single owner car. All service records available.' },
  { id: 2, name: 'Hyundai i20 Asta', year: 2020, price: '6.80', priceN: 680000, km: '45,000', fuel: 'Petrol', trans: 'Manual', owner: '1st', color: '#eef0f5', emoji: '🚙', verified: true, emi: '12,800', features: ['Sunroof', 'Rear Camera', 'ABS', 'Airbags'], city: 'Vadodara', desc: 'Top variant with sunroof. No accidents. Genuine seller.' },
  { id: 3, name: 'Honda City ZX CVT', year: 2019, price: '9.50', priceN: 950000, km: '58,000', fuel: 'Petrol', trans: 'Automatic', owner: '2nd', color: '#f0eef5', emoji: '🚘', verified: false, emi: '17,900', features: ['Cruise Control', 'Leather Seats', 'Lane Watch', 'Android Auto'], city: 'Vadodara', desc: 'Premium sedan in excellent condition. Service at Honda authorized center.' },
  { id: 4, name: 'Tata Nexon XZ+ Dark', year: 2022, price: '11.20', priceN: 1120000, km: '22,000', fuel: 'Diesel', trans: 'Manual', owner: '1st', color: '#eef5f0', emoji: '🛻', verified: true, emi: '21,100', features: ['Panoramic Sunroof', 'iRA Connected', 'Harman Audio', '6 Airbags'], city: 'Vadodara', desc: 'Latest model in dark edition. Under warranty till 2027.' },
  { id: 5, name: 'Kia Seltos HTX+ AT', year: 2021, price: '14.50', priceN: 1450000, km: '35,000', fuel: 'Petrol', trans: 'Automatic', owner: '1st', color: '#f5eef0', emoji: '🏎️', verified: true, emi: '27,300', features: ['Bose Audio', 'Ventilated Seats', '10.25" Screen', 'Drive Modes'], city: 'Ahmedabad', desc: 'Premium SUV with all luxury features. Full service history.' },
  { id: 6, name: 'Maruti Ertiga VXi CNG', year: 2020, price: '7.90', priceN: 790000, km: '52,000', fuel: 'CNG', trans: 'Manual', owner: '1st', color: '#eff5ee', emoji: '🚐', verified: false, emi: '14,900', features: ['7 Seater', 'Smart Play', 'Rear AC Vents', 'CNG Kit'], city: 'Vadodara', desc: 'Factory fitted CNG. Economy family car. Reasonable mileage.' },
  { id: 7, name: 'Toyota Fortuner 2.8 4x4', year: 2020, price: '28.50', priceN: 2850000, km: '48,000', fuel: 'Diesel', trans: 'Automatic', owner: '1st', color: '#f5f0ee', emoji: '🚙', verified: true, emi: '53,700', features: ['4x4', 'Multi Terrain Select', 'JBL Audio', 'Power Tailgate'], city: 'Surat', desc: 'Beast condition. All options available. Must see.' },
  { id: 8, name: 'Mahindra Thar LX 4x4', year: 2022, price: '17.80', priceN: 1780000, km: '15,000', fuel: 'Diesel', trans: 'Automatic', owner: '1st', color: '#eef2f5', emoji: '🛞', verified: true, emi: '33,500', features: ['4x4', 'Hardtop', 'Touchscreen', 'Rock Mode'], city: 'Vadodara', desc: 'Almost new. Diesel automatic with hard top. All accessories.' },
];

const DEFAULT_LEADS = [
  { name: 'Arjun Mehta', mobile: '98765-43210', car: 'Maruti Swift', budget: '4-6L', source: 'Website', stage: 'negotiation', assigned: 'Rahul S.', date: '12 Jun' },
  { name: 'Priya Shah', mobile: '87654-32109', car: 'Honda City', budget: '8-12L', source: 'Walk-in', stage: 'test-drive', assigned: 'Priya P.', date: '12 Jun' },
  { name: 'Kiran Patel', mobile: '76543-21098', car: 'Toyota Innova', budget: '15-20L', source: 'Referral', stage: 'new', assigned: 'Rahul S.', date: '11 Jun' },
  { name: 'Suresh Joshi', mobile: '65432-10987', car: 'Tata Nexon', budget: '10-12L', source: 'Social', stage: 'new', assigned: 'Amit J.', date: '11 Jun' },
  { name: 'Meera Trivedi', mobile: '54321-09876', car: 'Hyundai Creta', budget: '8-10L', source: 'Website', stage: 'contacted', assigned: 'Priya P.', date: '10 Jun' },
  { name: 'Rahul Gupta', mobile: '43210-98765', car: 'Kia Seltos', budget: '12-16L', source: 'Phone', stage: 'won', assigned: 'Rahul S.', date: '9 Jun' },
  { name: 'Anita Roy', mobile: '32109-87654', car: 'Maruti Baleno', budget: '5-7L', source: 'Website', stage: 'lost', assigned: 'Amit J.', date: '8 Jun' }
];

const DEFAULT_ENQUIRIES = [
  { name: 'Mohan Lal', car: 'Maruti Swift VXi 2021', query: 'Is first owner? Service history?', date: '12 Jun 2:30pm', status: 'new' },
  { name: 'Sunita Patel', car: 'Honda City ZX', query: 'What is lowest price possible?', date: '12 Jun 1:15pm', status: 'new' },
  { name: 'Vijay Shah', car: 'Tata Nexon XZ+', query: 'Still available? Can I test drive?', date: '11 Jun 4:00pm', status: 'replied' },
  { name: 'Kavita Mehta', car: 'Toyota Fortuner', query: 'Any warranty left? Exchange possible?', date: '11 Jun 11:30am', status: 'replied' },
  { name: 'Dilip Chauhan', car: 'Kia Seltos HTX', query: 'What accessories are included?', date: '10 Jun 3:45pm', status: 'closed' }
];

const DEFAULT_CUSTOMERS = [
  { name: 'Arjun Mehta', mobile: '+91 98765-43210', city: 'Vadodara', interests: 'Sedan, Budget 5-8L', purchases: '1', last: '12 Jun 2025' },
  { name: 'Priya Shah', mobile: '+91 87654-32109', city: 'Ahmedabad', interests: 'SUV, Automatic', purchases: '0', last: '12 Jun 2025' },
  { name: 'Kiran Patel', mobile: '+91 76543-21098', city: 'Vadodara', interests: 'MUV, Diesel', purchases: '2', last: '10 Jun 2025' },
  { name: 'Rahul Gupta', mobile: '+91 65432-10987', city: 'Surat', interests: 'Hatchback', purchases: '1', last: '9 Jun 2025' },
  { name: 'Meera Trivedi', mobile: '+91 54321-09876', city: 'Vadodara', interests: 'SUV, Petrol', purchases: '0', last: '10 Jun 2025' }
];

const DEFAULT_FOLLOWUPS = [
  { customer: 'Kiran Patel', car: 'Toyota Innova', due: 'Today 4:00 PM', type: 'Phone Call', notes: 'Discuss price drop', status: 'pending', assigned: 'Rahul S.' },
  { customer: 'Suresh Joshi', car: 'Tata Nexon', due: 'Today 6:00 PM', type: 'WhatsApp', notes: 'Send updated photos', status: 'pending', assigned: 'Amit J.' },
  { customer: 'Meera Trivedi', car: 'Hyundai Creta', due: 'Tomorrow 10AM', type: 'Test Drive', notes: 'Confirm time', status: 'scheduled', assigned: 'Priya P.' },
  { customer: 'Dilip Chauhan', car: 'Kia Seltos', due: 'Yesterday', type: 'Phone Call', notes: 'Follow up on offer', status: 'overdue', assigned: 'Rahul S.' },
  { customer: 'Mohan Lal', car: 'Swift VXi', due: '13 Jun 2PM', type: 'Visit', notes: 'Show car', status: 'scheduled', assigned: 'Amit J.' }
];

const DEFAULT_REVENUE = [
  { date: '12 Jun', car: 'Maruti Swift VXi 2021', buyer: 'Arjun Mehta', sale: '₹5.20L', cost: '₹4.10L', profit: '₹1.10L', mode: 'Bank Transfer' },
  { date: '10 Jun', car: 'Kia Seltos HTX', buyer: 'Rahul Gupta', sale: '₹14.50L', cost: '₹12.80L', profit: '₹1.70L', mode: 'Loan (HDFC)' },
  { date: '8 Jun', car: 'Honda Amaze S', buyer: 'Sunita Patel', sale: '₹7.20L', cost: '₹6.30L', profit: '₹0.90L', mode: 'Cash' },
  { date: '6 Jun', car: 'Tata Harrier XZ', buyer: 'Vikram Shah', sale: '₹17.80L', cost: '₹16.00L', profit: '₹1.80L', mode: 'Loan (SBI)' },
  { date: '4 Jun', car: 'Maruti Dzire ZXi', buyer: 'Pooja Mehta', sale: '₹8.10L', cost: '₹7.20L', profit: '₹0.90L', mode: 'Bank Transfer' }
];

const DEFAULT_STAFF = [
  { name: 'Rajesh Patel', email: 'rajesh@marketguruhp.in', role: 'Super Admin', dept: 'Management', status: 'active', last: 'Just now' },
  { name: 'Rahul Sharma', email: 'rahul@marketguruhp.in', role: 'Sales Manager', dept: 'Sales', status: 'active', last: '10 min ago' },
  { name: 'Priya Patel', email: 'priya@marketguruhp.in', role: 'Executive', dept: 'Sales', status: 'active', last: '1 hr ago' },
  { name: 'Amit Joshi', email: 'amit@marketguruhp.in', role: 'Executive', dept: 'Sales', status: 'active', last: '2 hr ago' },
  { name: 'Neha Verma', email: 'neha@marketguruhp.in', role: 'Finance', dept: 'Finance', status: 'active', last: 'Yesterday' },
  { name: 'Deepak Shah', email: 'deepak@marketguruhp.in', role: 'Executive', dept: 'Sales', status: 'inactive', last: '3 days ago' }
];

// Database API connector settings
const apiBase = 'http://localhost:5000/api';
let isBackendConnected = false;

// Local Memory State Cache loaded from Backend or local storage
let carsState = [];
let leadsState = [];
let enquiriesState = [];
let customersState = [];
let followupsState = [];
let revenueState = [];
let staffState = [];
let wishlistState = [];
let subscriptionsState = [];

// Helper to load/save JSON from localStorage (used in fallback mode)
function getDB(key, defaultValue) {
  const data = localStorage.getItem(key);
  if (!data) {
    localStorage.setItem(key, JSON.stringify(defaultValue));
    return defaultValue;
  }
  try {
    return JSON.parse(data);
  } catch (e) {
    return defaultValue;
  }
}

function saveDB(key, data) {
  localStorage.setItem(key, JSON.stringify(data));
}

// Synchronous HTTP Request helper for initial data load
function requestSync(method, endpoint, payload = null) {
  try {
    const xhr = new XMLHttpRequest();
    xhr.open(method, `${apiBase}/${endpoint}`, false); // false makes it synchronous
    if (payload) {
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.send(JSON.stringify(payload));
    } else {
      xhr.send(null);
    }
    if (xhr.status >= 200 && xhr.status < 300) {
      return JSON.parse(xhr.responseText);
    }
  } catch (e) {
    console.error(`Sync request to /${endpoint} failed:`, e);
  }
  return null;
}

// Asynchronous HTTP Request helper for write operations
async function requestAsync(method, endpoint, payload = null) {
  try {
    const response = await fetch(`${apiBase}/${endpoint}`, {
      method: method,
      headers: { 'Content-Type': 'application/json' },
      body: payload ? JSON.stringify(payload) : null
    });
    if (response.ok) {
      return await response.json();
    }
  } catch (e) {
    console.error(`Async request to /${endpoint} failed:`, e);
  }
  return null;
}

// Initialize database connection
function initializeDatabase() {
  // Directly request init to test connection and fetch data in one single roundtrip
  try {
    const initData = requestSync('GET', 'init');
    if (initData && initData.status === 'success') {
      isBackendConnected = true;
      carsState = initData.cars;
      leadsState = initData.leads;
      enquiriesState = initData.enquiries;
      customersState = initData.customers;
      followupsState = initData.followups;
      revenueState = initData.revenue;
      staffState = initData.staff;
      wishlistState = initData.wishlist;
      subscriptionsState = initData.subscriptions;
      console.log("MySQL Flask backend is connected and data synchronized successfully!");
      return;
    }
  } catch (e) {
    console.log("MySQL Flask backend not running or init failed. Falling back to LocalStorage.");
  }

  isBackendConnected = false;
  // Fallback to localStorage mock database
  const userCars = getDB('mg_user_cars', []);
  carsState = [...DEFAULT_USED_CARS, ...userCars];
  leadsState = getDB('mg_leads', DEFAULT_LEADS);
  enquiriesState = getDB('mg_enquiries', DEFAULT_ENQUIRIES);
  customersState = getDB('mg_customers', DEFAULT_CUSTOMERS);
  followupsState = getDB('mg_followups', DEFAULT_FOLLOWUPS);
  revenueState = getDB('mg_revenue', DEFAULT_REVENUE);
  staffState = getDB('mg_staff', DEFAULT_STAFF);
}

// Perform initial synchronization
initializeDatabase();

// Database Interface Implementation
const db = {
  isBackendOnline: () => isBackendConnected,
  getApiBase: () => apiBase,

  getUsedCars: () => {
    return carsState;
  },
  getNewCars: () => [],
  getLeads: () => {
    return leadsState;
  },
  getEnquiries: () => {
    return enquiriesState;
  },
  getCustomers: () => {
    return customersState;
  },
  getFollowups: () => {
    return followupsState;
  },
  getRevenue: () => {
    return revenueState;
  },
  getStaff: () => {
    return staffState;
  },

  getCarById: (id) => {
    id = parseInt(id);
    const car = carsState.find(c => c.id === id);
    if (car) return { ...car, isNew: false };
    return null;
  },

  addUserCar: (car) => {
    // Standardize input fields
    car.verified = car.verified || false;
    car.color = car.color || '#e8eef5';
    car.emoji = car.emoji || '🚗';
    car.features = typeof car.features === 'string' ? car.features.split(',').map(s => s.trim()) : (car.features || []);

    if (isBackendConnected) {
      // Send write to API
      const result = requestSync('POST', 'cars', {
        name: car.name,
        year: car.year,
        price: car.price,
        priceN: car.priceN,
        km: car.km,
        fuel: car.fuel,
        trans: car.trans,
        owner: car.owner,
        color: car.color,
        emoji: car.emoji,
        city: car.city,
        desc: car.desc,
        features: car.features,
        verified: car.verified ? 1 : 0,
        listed_by: localStorage.getItem('mg_current_user_mobile')
      });
      if (result && result.status === 'success') {
        carsState.push(result.car);
        return result.car;
      }
    }

    // Local Storage Fallback
    const userCars = getDB('mg_user_cars', []);
    const nextId = 1000 + userCars.length;
    car.id = nextId;
    car.emi = car.emi || Math.round(car.priceN * 0.019).toLocaleString('en-IN') + '/mo';
    userCars.push(car);
    saveDB('mg_user_cars', userCars);
    carsState.push(car);
    return car;
  },

  addEnquiry: (enquiry) => {
    enquiry.date = enquiry.date || new Date().toLocaleString('en-IN', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });
    enquiry.status = 'new';

    if (isBackendConnected) {
      const result = requestSync('POST', 'enquiries', enquiry);
      if (result && result.status === 'success') {
        enquiriesState.unshift(result.enquiry);
        // Refresh leads as adding an enquiry creates a lead on the backend
        const leadsRes = requestSync('GET', 'init');
        if (leadsRes && leadsRes.status === 'success') {
          leadsState = leadsRes.leads;
        }
        return;
      }
    }

    // Local Storage Fallback
    const enquiries = getDB('mg_enquiries', DEFAULT_ENQUIRIES);
    enquiries.unshift(enquiry);
    saveDB('mg_enquiries', enquiries);
    enquiriesState = enquiries;

    const leads = getDB('mg_leads', DEFAULT_LEADS);
    leads.unshift({
      name: enquiry.name,
      mobile: enquiry.mobile || '98765-XXXXX',
      car: enquiry.car,
      budget: enquiry.budget || 'Any',
      source: 'Website',
      stage: 'new',
      assigned: 'Rahul Sharma',
      date: new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })
    });
    saveDB('mg_leads', leads);
    leadsState = leads;
  },

  getWishlist: () => {
    const loggedMobile = localStorage.getItem('mg_current_user_mobile') || '';
    if (isBackendConnected && loggedMobile) {
      return wishlistState.filter(w => w.user_mobile === loggedMobile).map(w => w.car_id);
    }
    return getDB('mg_wishlist', []);
  },

  toggleWishlist: (id) => {
    id = parseInt(id);
    const loggedMobile = localStorage.getItem('mg_current_user_mobile') || '';

    if (isBackendConnected && loggedMobile) {
      const result = requestSync('POST', 'wishlist/toggle', {
        user_mobile: loggedMobile,
        car_id: id
      });
      if (result && result.status === 'success') {
        // Reload wishlist entries
        const res = requestSync('GET', 'init');
        if (res && res.status === 'success') {
          wishlistState = res.wishlist;
        }
        return result.added;
      }
    }

    // Fallback
    let wishlist = getDB('mg_wishlist', []);
    if (wishlist.includes(id)) {
      wishlist = wishlist.filter(x => x !== id);
      saveDB('mg_wishlist', wishlist);
      return false;
    } else {
      wishlist.push(id);
      saveDB('mg_wishlist', wishlist);
      return true;
    }
  },

  isWishlisted: (id) => {
    id = parseInt(id);
    return db.getWishlist().includes(id);
  },

  activateSubscription: (userMobile) => {
    if (isBackendConnected) {
      const result = requestSync('POST', 'subscription/activate', { user_mobile: userMobile });
      if (result && result.status === 'success') {
        // Refresh subscriptions cache
        const res = requestSync('GET', 'init');
        if (res && res.status === 'success') {
          subscriptionsState = res.subscriptions;
        }
        return;
      }
    }

    // Fallback
    localStorage.setItem('mg_sub_status_' + userMobile, 'active');
    const expiry = new Date();
    expiry.setDate(expiry.getDate() + 30);
    localStorage.setItem('mg_sub_expiry_' + userMobile, expiry.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }));
  },

  cancelSubscription: (userMobile) => {
    if (isBackendConnected) {
      const result = requestSync('POST', 'subscription/cancel', { user_mobile: userMobile });
      if (result && result.status === 'success') {
        // Refresh subscriptions cache
        const res = requestSync('GET', 'init');
        if (res && res.status === 'success') {
          subscriptionsState = res.subscriptions;
        }
        return;
      }
    }

    // Fallback
    localStorage.setItem('mg_sub_status_' + userMobile, 'inactive');
    localStorage.removeItem('mg_sub_expiry_' + userMobile);
  },

  getSubscriptionDetails: (userMobile) => {
    if (isBackendConnected) {
      const sub = subscriptionsState.find(s => s.user_mobile === userMobile);
      if (sub) {
        return { status: sub.status, expiry: sub.expiry };
      }
      return { status: 'none', expiry: null };
    }

    // Fallback
    const status = localStorage.getItem('mg_sub_status_' + userMobile) || 'none';
    const expiry = localStorage.getItem('mg_sub_expiry_' + userMobile) || null;
    return { status, expiry };
  },

  addLead: (lead) => {
    if (isBackendConnected) {
      const result = requestSync('POST', 'leads', lead);
      if (result && result.status === 'success') {
        leadsState.unshift(result.lead);
        // Refresh customers as adding a lead updates customers table
        const res = requestSync('GET', 'init');
        if (res && res.status === 'success') {
          customersState = res.customers;
        }
        return;
      }
    }

    // Fallback
    const leads = getDB('mg_leads', DEFAULT_LEADS);
    leads.unshift(lead);
    saveDB('mg_leads', leads);
    leadsState = leads;
  },

  // Missing Write Operations Added for Admin Console Synchronization
  toggleVerifyCar: (id, verified) => {
    id = parseInt(id);
    if (isBackendConnected) {
      const result = requestSync('POST', 'cars/verify', { car_id: id, verified: verified ? 1 : 0 });
      if (result && result.status === 'success') {
        const car = carsState.find(c => c.id === id);
        if (car) car.verified = verified;
        return true;
      }
    }

    // Fallback
    const userCars = getDB('mg_user_cars', []);
    const idx = userCars.findIndex(c => c.id === id);
    if (idx !== -1) {
      userCars[idx].verified = verified;
      saveDB('mg_user_cars', userCars);
      const car = carsState.find(c => c.id === id);
      if (car) car.verified = verified;
      return true;
    }
    return false;
  },

  markSold: (id) => {
    id = parseInt(id);
    if (isBackendConnected) {
      const result = requestSync('POST', 'cars/sold', { car_id: id });
      if (result && result.status === 'success') {
        carsState = carsState.filter(c => c.id !== id);
        return true;
      }
    }

    // Fallback
    const userCars = getDB('mg_user_cars', []);
    const idx = userCars.findIndex(c => c.id === id);
    if (idx !== -1) {
      userCars.splice(idx, 1);
      saveDB('mg_user_cars', userCars);
      carsState = carsState.filter(c => c.id !== id);
      return true;
    }
    return false;
  },

  resolveEnquiry: (customerName) => {
    if (isBackendConnected) {
      const result = requestSync('POST', 'enquiries/resolve', { name: customerName });
      if (result && result.status === 'success') {
        const enq = enquiriesState.find(e => e.name === customerName);
        if (enq) enq.status = 'replied';
        return true;
      }
    }

    // Fallback
    const enquiries = getDB('mg_enquiries', DEFAULT_ENQUIRIES);
    const idx = enquiries.findIndex(e => e.name === customerName);
    if (idx !== -1) {
      enquiries[idx].status = 'replied';
      saveDB('mg_enquiries', enquiries);
      const enq = enquiriesState.find(e => e.name === customerName);
      if (enq) enq.status = 'replied';
      return true;
    }
    return false;
  },

  addStaff: (staffMember) => {
    if (isBackendConnected) {
      const result = requestSync('POST', 'staff', staffMember);
      if (result && result.status === 'success') {
        staffState.push(result.staff);
        return result.staff;
      }
    }

    // Fallback
    const staff = getDB('mg_staff', DEFAULT_STAFF);
    staff.push(staffMember);
    saveDB('mg_staff', staff);
    staffState.push(staffMember);
    return staffMember;
  }
};

// Expose globally
window.mgDB = db;
