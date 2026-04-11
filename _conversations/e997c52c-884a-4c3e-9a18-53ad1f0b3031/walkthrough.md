# NIBMX Vault & Blockchain — Security Hardening Walkthrough

## Changes Made

### 1. API Security Fixes — [vault.mjs](file:///c:/Users/OMEN/Documents/kibx/api/_routes/vault.mjs)

**DB Transactions** — 8 mutation endpoints now use `pool.connect()` + `BEGIN/COMMIT/ROLLBACK`:
- `POST /vault/deposit`, `POST /vault/withdraw`, `POST /vault/transfer`
- `POST /tokens/mint`, `POST /tokens/transfer`, `POST /tokens/redeem`
- `PUT /admin/vault/withdrawals/:id` (approve/reject)
- `PUT /admin/vault/withdrawals/:id/process`

**Row Locking** — `SELECT ... FOR UPDATE` added to all balance reads:
- Prevents race conditions from concurrent requests reading stale balances
- Applied to `vault_accounts` and `gold_tokens` rows before mutations

**Input Validation** — 6 Zod schemas:
| Schema | Validates | Key Rules |
|--------|----------|-----------|
| `depositSchema` | `/vault/deposit` | `amount_grams` > 0, max 50,000g |
| `withdrawSchema` | `/vault/withdraw` | `delivery_address` min 5 chars |
| `mintSchema` | `/tokens/mint` | `weight_grams` > 0, max 50,000g |
| `tokenTransferSchema` | `/tokens/transfer` | valid email, `token_id` required |
| `redeemSchema` | `/tokens/redeem` | `token_id` required |
| `vaultTransferSchema` | `/vault/transfer` | valid email, amount > 0 |

---

### 2. Rate Limiting — [index.mjs](file:///c:/Users/OMEN/Documents/kibx/api/index.mjs)

Added `vaultLimiter` (10 requests/minute per IP) on 6 mutation endpoints, more restrictive than the global API limiter (100/15min).

---

### 3. Dependencies — [package.json](file:///c:/Users/OMEN/Documents/kibx/package.json)

Added `zod@^3.24.0` for runtime input validation.

---

### 4. Internal Documentation — [index.html](file:///c:/Users/OMEN/Documents/kibx/index.html)

Added 3 new sections under the Vault & Blockchain documentation:
- **`#blockchain-stacks`** — Competitor blockchain stack comparison (9 platforms × 6 columns + feature matrix)
- **`#vault-security`** — Production readiness table (8 items) + stack recommendations (8 rows) + security audit callout

## Verification
- `zod@3.24.0` installed successfully
- All 8 mutation endpoints refactored with consistent `client.query('BEGIN')` → `client.query('COMMIT')` → `ROLLBACK` → `client.release()` pattern
- Sidebar navigation updated with "Competitor Stacks" and "Security Hardening" links
