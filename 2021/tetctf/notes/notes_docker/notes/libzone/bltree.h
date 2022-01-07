/*
 * Author: peter
 * Balance Tree Implemenation
 */
#ifndef _BLTREE_H
#define _BLTREE_H

#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>
#include <sys/cdefs.h>

__BEGIN_DECLS
struct BLNode;
typedef struct BLNode* BLNode_t;

struct BLNode
{
	int64_t height;
	BLNode_t left;
	BLNode_t right;
};

#define BLTREE_ROOT_DECL(var_name) struct BLNode var_name

#define OBJECT_AS_BLTNODE(objectp, bl_node_member, object_t) \
		((BLNode_t)((size_t)objectp + offsetof(object_t, bl_node_member)))
#define BLTNODE_AS_OBJECT(bl_node_p, bl_node_member, object_t) \
		((object_t *)((size_t)bl_node_p - offsetof(object_t, bl_node_member)))

#define BLNHEIGHT(a_node_p) (a_node_p != NULL ? a_node_p->height : 0)
#define BLNBALANCE(a_node_p) (BLNHEIGHT(a_node_p->left) - BLNHEIGHT(a_node_p->right))

BLNode_t BLTInsert(BLNode_t root, BLNode_t a_node, int (*cmp)(BLNode_t, BLNode_t));
BLNode_t BLTDelete(BLNode_t root, BLNode_t a_node, 
		int (*cmp)(BLNode_t, BLNode_t), void (*deallocObject)(BLNode_t),
		void (*swap)(BLNode_t, BLNode_t));
BLNode_t BLTSearch(BLNode_t root, BLNode_t a_node, int (*cmp)(BLNode_t, BLNode_t));
uint32_t BLTIsBalance(BLNode_t root);
BLNode_t BLTDestroy(BLNode_t root, void (*deallocObject)(BLNode_t));

void BLTPrint(BLNode_t root, void (*printObject)(BLNode_t));
void BLTNodeInit(BLNode_t a_node);

__END_DECLS
#endif
