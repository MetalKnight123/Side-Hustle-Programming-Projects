const { Client } = require('pg');
const fs = require('fs');

async function run() {
  const conn = process.env.PGCONN;
  if (!conn) {
    console.error('PGCONN env var not set');
    process.exit(2);
  }
  const sql = fs.readFileSync('supabase/init.sql', 'utf8');
  const client = new Client({ connectionString: conn });
  try {
    await client.connect();
    console.log('Connected. Executing SQL...');
    await client.query(sql);
    console.log('SQL executed successfully.');
  } catch (err) {
    console.error('SQL execution error:', err && err.message ? err.message : err);
    process.exit(1);
  } finally {
    await client.end();
  }
}

run();
